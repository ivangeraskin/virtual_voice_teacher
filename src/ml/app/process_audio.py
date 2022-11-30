import requests

from typing import Dict

from utils import prepare_audio_file, recognize_audio, add_punctuation_to_recognize_text, filler_word_analyse, get_logger
from settings import FILLER_WORLDS, debug

from logging.handlers import RotatingFileHandler
from settings import get_logger
logger = get_logger(logger_name=__file__,
                    handler_adds=RotatingFileHandler(filename="logs/output.logs", maxBytes=2**20))


def process(file_pth: str) -> Dict:
    mp3_raw_data = prepare_audio_file(audio_file_path=file_pth)

    response = requests.post("http://localhost:8080/recognize", data=mp3_raw_data)
    response.raise_for_status()
    recognized_text = response.json().get('recognized_text')

    text_for_ml = add_punctuation_to_recognize_text(recognized_text=recognized_text)
    text_for_user = filler_word_analyse(text=text_for_ml, filler_words=FILLER_WORLDS)
    return {"message": text_for_user}


if __name__ == '__main__':
    for file_pth in ("/home/urev/projects/virtual_voice_teacher/data/audio-2022-11-30 14:30:02.967816.wav",
                     "/home/urev/projects/virtual_voice_teacher/data/audio-2022-11-30 16:32:32.366352.wav",
                     "/home/urev/projects/virtual_voice_teacher/data/processed/10_kazinik_10sec.mp3",
                     "/home/urev/projects/virtual_voice_teacher/data/processed/10_restavrator_10sec.mp3"):
        logger.info(f"Started with file: {file_pth}")
        msg = process(file_pth=file_pth)
        logger.debug(f"Result: {msg}")
