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
from settings import BOT_TOKEN, RABBIT_URL, RABBIT_PORT, DB_URL
import datetime as dt
import os
from aio_pika import connect_robust
from aio_pika.patterns import RPC
import requests

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
    await message.answer("Доброго времени суток! Расскажите о чем-нибудь в аудиосообщении. Рекомендуемое время записи - 1-2 минуты. Выбирайте любую тему: хобби, интересный проект, идеальный отпуск, ...")

async def handle_file(file, file_name: str, path: str):
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")

@dp.message_handler(content_types=ContentType.VOICE)
async def process_audio(message: Message):
    await message.answer("Ваша запись обрабатывается")

    file_name = f"audio-{dt.datetime.now()}.ogg"
    audio_path = os.path.join(path_voice, file_name)

    voice = await message.voice.get_file()
    await handle_file(file=voice, file_name=file_name, path=path_voice)
    connection = await connect_robust(host=RABBIT_URL, port=RABBIT_PORT)

    async with connection:
        # Creating channel
        channel = await connection.channel()
        rpc = await RPC.create(channel)
        reply = await rpc.call("v", kwargs=dict(file_pth=audio_path))
        await message.answer(reply.get("message"))

    # add record to db here
    db_record = {"tg_id": message.from_id,
                 "tg_name": message.from_user.mention,
                 "file_id": message.voice.file_id,
                 "comments": reply.get("message")}
    requests.post(url=DB_URL+"/add_review", json=db_record)
    print(db_record)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()