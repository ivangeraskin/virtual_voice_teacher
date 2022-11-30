import json

import subprocess

import numpy as np

from functools import lru_cache

from typing import List
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

from settings import AUDIO_FRAME_RATE, N_AUDIO_CHANNELS
from settings import get_logger
logger = get_logger(logger_name=__file__)


@lru_cache(maxsize=32)
def get_model():
    SetLogLevel(0)
    m = Model("model")
    rec = KaldiRecognizer(m, AUDIO_FRAME_RATE)
    rec.SetWords(True)
    return rec


def prepare_audio_file(audio_file_path: str):
    mp3 = AudioSegment.from_file(audio_file_path, format='ogg')
    if audio_file_path.split(".")[-1] == 'wav_':
        #TODO необходимо, тк *.wav файлы от телеграма по-умолчанию, выдают пустоту
        # ниже выполняется их пересохранение в mp3
        mp3.export(audio_file_path.replace('.wav', '.mp3'), format="mp3")
        mp3 = AudioSegment.from_file(audio_file_path.replace('.wav', '.mp3'))
    mp3 = mp3.set_channels(N_AUDIO_CHANNELS)
    mp3 = mp3.set_frame_rate(AUDIO_FRAME_RATE)
    return mp3.raw_data


def recognize_audio(mp3_raw_data, model) -> str:
    model.AcceptWaveform(mp3_raw_data)
    result = model.Result()
    text = json.loads(result)["text"]
    return text


def add_punctuation_to_recognize_text(recognized_text: str):
    # Добавляем пунктуацию
    cased = subprocess.check_output('python3 recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True,
                                    text=True, input=recognized_text)

    return json.dumps(cased, ensure_ascii=False, indent=4)


def filler_word_analyse(text: str, filler_words: List[str])-> str:
    filler_cnt_dict = {}

    # Для каждого слова-паразита считаем кол-во вхождений
    for filler in filler_words:
        filler_cnt = text.count(' ' + filler + ' ')
        if filler_cnt > 0:
            filler_cnt_dict[filler] = filler_cnt

    # Сортируем от максимального кол-ва вхождений к минимальному
    filler_cnt_dict = {k: v for k, v in sorted(filler_cnt_dict.items(), key=lambda item: -item[1])}

    # Общее количество слов
    all_words_cnt = text.count(' ') + 1

    # Количество слов-паразитов
    all_fillers_cnt = sum(filler_cnt_dict.values())

    # Доля филеров в процентах
    fillers_pct = 100 * all_fillers_cnt / all_words_cnt

    all_words = 'Всего слов - ' + str(all_words_cnt) + ' \n \n'
    filler_words_pct = 'Доля слов паразитов - ' + str(np.round(fillers_pct, 1)) + '% \n \n'
    frequent_fillers = 'Встречаемость слов-паразитов: \n'

    for filler in filler_cnt_dict:
        filler_frequency = filler + ' - ' + str(filler_cnt_dict[filler]) + '\n'
        frequent_fillers = frequent_fillers + filler_frequency

    if all_words == 0:
        text_for_user = 'В записи не обнаружено ни одного слова, предлагаем сделать еще одну попытку. Говорите, не стесняйтесь)'
    elif all_fillers_cnt == 0:
        text_for_user = 'В записи не обнаружено ни одного мусорного слова. Так держать. Расскажите еще что-нибудь) \n \n' + all_words
    elif fillers_pct <= 1:
        conclusion = 'В вашей речи немного мусорных слов, но кое-что мы нашли. \n \n'
        text_for_user = conclusion + all_words + filler_words_pct + frequent_fillers
    elif 1 < fillers_pct <= 3:
        conclusion = 'Слов-паразитов в вашей речи среднее количество, предлагаем еще потренироваться говорить без них. Продолжайте! \n \n'
        text_for_user = conclusion + all_words + filler_words_pct + frequent_fillers
    elif fillers_pct > 3:
        conclusion = 'Слов-паразитов в вашей речи достаточно много, предлагаем потренироваться говорить без них. Продолжайте! \n \n'
        text_for_user = conclusion + all_words + filler_words_pct + frequent_fillers

    return text_for_user


if __name__ == '__main__':
    pass