import os

from functools import wraps

import logging
from logging import StreamHandler


def debug(func):
    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        logger = get_logger(logger_name=__file__)
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logger.debug(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug


def get_logger(logger_name="super_logger", handler_adds=None):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    super_logger = logging.getLogger(logger_name)
    super_logger.setLevel(logging.DEBUG)
    handler = StreamHandler()
    handler.setFormatter(fmt=formatter)
    super_logger.addHandler(handler)

    if not handler_adds is None:
        handler_adds.setFormatter(fmt=formatter)
        handler_adds.setLevel(logging.DEBUG)
        super_logger.addHandler(handler_adds)
    return super_logger


RABBIT_URL = os.getenv("RABBIT_URL")
RABBIT_PORT = os.getenv("RABBIT_PORT")
SHARED_FOLDER_PATH = "/voice"

AUDIO_FRAME_RATE = 48000
N_AUDIO_CHANNELS = 1

FILLER_WORLDS = ['да',
                 'точка',
                 'это самое',
                 'типо того',
                 'таки',
                 'собственно говоря',
                 'прямо',
                 'прикол',
                 'практически',
                 'походу',
                 'на самом деле',
                 'конкретно',
                 'как-то так',
                 'как сказать',
                 'как его',
                 'итак',
                 'знаешь',
                 'да ладно',
                 'все такое',
                 'в самом деле',
                 'в натуре',
                 'вот',
                 'эм',
                 'ну',
                 'вообще-то',
                 'так сказать',
                 'кстати',
                 'в общем',
                 'просто',
                 'ааа',
                 'мм',
                 'стало быть']