from typing import Dict
from settings import FILLER_WORLDS
import json
import numpy as np
from typing import List
from pydub import AudioSegment
from settings import AUDIO_FRAME_RATE, N_AUDIO_CHANNELS
import logging
from utils import get_model

logger = logging.getLogger(__file__)

def process(file_pth: str) -> Dict:
    model = get_model()
    mp3_raw_data = prepare_audio_file(audio_file_path=file_pth)
    recognized_text, duration_sec = recognize_audio(mp3_raw_data, model)
    logger.info(recognized_text)
    text_freq_analyse = speech_frequency(text, duration_sec)
    text_filler_analyse = filler_word_analyse(text=recognized_text, filler_words=FILLER_WORLDS)
    text_for_user = text_freq_analyse + text_filler_analyse
    return {"message": text_for_user}

def prepare_audio_file(audio_file_path: str):
    ogg_file = AudioSegment.from_file(audio_file_path)
    mp3_path = audio_file_path.replace(".ogg", ".mp3")
    ogg_file.export(mp3_path, format="mp3")
    return mp3_path


def recognize_audio(file_pth, model) -> str:
    mp3_file = AudioSegment.from_file(file_pth)
    mp3_file = mp3_file.set_channels(N_AUDIO_CHANNELS) \
                       .set_frame_rate(AUDIO_FRAME_RATE)
    model.AcceptWaveform(mp3_file.raw_data)
    result = model.Result()
    text = json.loads(result)["text"]
    duration_sec = mp3_file.duration_seconds
    return text, duration_sec

def speech_frequency(text, duration_sec):
    
    words_per_min = int(len(text.split(' '))*60/duration_sec)
    
    if words_per_min<90:
        text_for_user = 'Cкорость вашей речи - ' + str(words_per_min) + ' слов в минуту. Рекомендуем говорить немного динамичнее. Нормальная скорость - 120 слов в минуту.'
    elif words_per_min>150:
        text_for_user = 'Cкорость вашей речи - ' + str(words_per_min) + ' слов в минуту. Рекомендуем говорить немного медленнее. Нормальная скорость - 90-150 слов в минуту.'
    else:
        text_for_user = 'Cкорость вашей речи - ' + str(words_per_min) + ' слов в минуту. Это в пределах нормы.'
        
    return text_for_user + '\n\n'

def filler_word_analyse(text: str, filler_words: List[str])-> str:
    filler_cnt_dict = {}

    # Для каждого слова-паразита считаем кол-во вхождений
    for filler in filler_words:
        # Если в середине
        filler_cnt = text.count(' '+filler+' ')
        # Если в начале
        if text[:len(filler+' ')] == filler+' ':
            filler_cnt =+ 1
        # Если в конце
        if text[-len(' '+filler):] ==' '+filler:
            filler_cnt =+ 1 
        if filler_cnt>0:
            filler_cnt_dict[filler] = filler_cnt

    # Сортируем от максимального кол-ва вхождений к минимальному
    filler_cnt_dict = {k: v for k, v in sorted(filler_cnt_dict.items(), key=lambda item: -item[1])}

    # Общее количество слов
    all_words_cnt = text.count(' ') + 1

    # Количество слов-паразитов
    all_fillers_cnt = sum(filler_cnt_dict.values())

    # Доля филеров в пadd_punctuation_to_recognize_text, роцентах
    fillers_pct = 100 * all_fillers_cnt / all_words_cnt

    all_words = 'Всего слов - ' + str(all_words_cnt) + ' \n \n'
    filler_words_pct = 'Доля слов паразитов - ' + str(np.round(fillers_pct, 1)) + '% \n \n'
    frequent_fillers = 'Встречаемость слов-паразитов: \n'

    for filler in filler_cnt_dict:
        filler_frequency = filler + ' - ' + str(filler_cnt_dict[filler]) + '\n'
        frequent_fillers = frequent_fillers + filler_frequency

    if len(text) == 0:
        text_for_user = 'В записи не обнаружено ни одного слова, предлагаем сделать еще одну попытку. Говорите, не стесняйтесь)'
    elif all_fillers_cnt == 0:
        text_for_user = 'В записи не обнаружено ни одного слова-паразита. Так держать. Расскажите еще что-нибудь) \n \n' + all_words
    elif fillers_pct <= 1:
        conclusion = 'В вашей речи немного слов-паразитов, но кое-что мы нашли. \n \n'
        text_for_user = conclusion + all_words + filler_words_pct + frequent_fillers
    elif 1 < fillers_pct <= 3:
        conclusion = 'Слов-паразитов в вашей речи среднее количество, предлагаем еще потренироваться говорить без них. Продолжайте! \n \n'
        text_for_user = conclusion + all_words + filler_words_pct + frequent_fillers
    elif fillers_pct > 3:
        conclusion = 'Слов-паразитов в вашей речи достаточно много, предлагаем потренироваться говорить без них. Продолжайте! \n \n'
        text_for_user = conclusion + all_words + filler_words_pct + frequent_fillers

    return text_for_user


def test_audio():
    data_pth = "/voice/audio-2022-12-06 23:14:33.081970.mp3"
    model = get_model()
    text = recognize_audio(data_pth, model)
    print(text)
    text_for_user = filler_word_analyse(text=text, filler_words=FILLER_WORLDS)
    print(text_for_user)

def test_cnt():
    s = "ну вот получается как-то так"
    text_for_user = filler_word_analyse(text=s, filler_words=FILLER_WORLDS)

if __name__ == "__main__":
    test_cnt()
