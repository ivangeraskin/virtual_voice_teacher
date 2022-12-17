from functools import lru_cache
from vosk import Model, KaldiRecognizer, SetLogLevel

from settings import AUDIO_FRAME_RATE, N_AUDIO_CHANNELS

import logging


def setup_logging(logfile='log.txt', loglevel='DEBUG'):
    """

    :param logfile:
    :param loglevel:
    :return:
    """
    loglevel = getattr(logging, loglevel)

    logger = logging.getLogger()
    logger.setLevel(loglevel)
    fmt = '%(asctime)s: %(levelname)s: %(filename)s: ' + \
          '%(funcName)s(): %(lineno)d: %(message)s'
    formatter = logging.Formatter(fmt)

    fh = logging.FileHandler(logfile, encoding='utf-8')
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

@lru_cache(maxsize=32)
def get_model():
    SetLogLevel(0)
    m = Model("model")
    rec = KaldiRecognizer(m, AUDIO_FRAME_RATE)
    rec.SetWords(True)
    return rec