import logging
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ParseMode
from aiogram.types import ContentType
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import text, bold
from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from settings import BOT_TOKEN, RABBIT_URL, RABBIT_PORT
import datetime as dt
import os
from aio_pika import connect_robust
from aio_pika.patterns import RPC

_logger = logging.getLogger(__name__)
path_voice = "/voice/"


def init_bot():
    """
    """
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())
    return bot, dp

bot, dp = init_bot()

#async def on_startup(dp):
#    _logger.warning('Starting connection. ')
#    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    _logger.warning('Bye! Shutting down webhook connection')
    bot.close()

@dp.message_handler(content_types=ContentType.TEXT)
async def process_text(message: Message):
    await message.answer("Привет!")

@dp.message_handler(content_types=ContentType.VOICE)
async def process_audio(message: Message):
    await message.answer("Аудил")

    file_name = f"audio-{dt.datetime.now()}.wav"
    audio_path = os.path.join(path_voice, file_name)

    await message.voice.download(audio_path)
    connection = await connect_robust(host=RABBIT_URL, port=RABBIT_PORT)

    async with connection:
        # Creating channel
        channel = await connection.channel()
        rpc = await RPC.create(channel)
        c = await rpc.call("v", kwargs=dict(file_pth=audio_path))
        await message.answer(c)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()