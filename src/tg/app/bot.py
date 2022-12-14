import logging
import os
import datetime as dt
import pika
import json
import asyncio

from telegram import Update,  ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters, CallbackContext
from aio_pika import connect_robust
from aio_pika.patterns import RPC


from classes import Users
import templates
from settings import BOT_TOKEN, RABBIT_URL, RABBIT_PORT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

UsersData = Users()

path_voice = "/voice/"

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

if not os.path.exists(path_voice):
    os.makedirs(path_voice)


def start_block(update: Update, context: CallbackContext) -> None:
    '''
    Старт диалога.

    Args:
        update (Update)
        context (CallbackContext)

    При "/start" сразу переведёт "stage" в режим ожидания гс, 
    а также отправит шаблоны для разговора
    '''
    user = update.effective_user
    UsersData.check_user(user)
    name = f"Привет, {user.first_name}!\n"
    UsersData.edit_stage(user, "Wait_voice")
    update.message.reply_html(name + templates.message_greeting)
    update.message.reply_text(templates.message_topics)


def main_block(update: Update, context: CallbackContext) -> None:
    '''
    Args:
        update (Update)
        context (CallbackContext)

    Сразу переведёт "stage" в режим ожидания гс, 
    а также отправит шаблоны для разговора
    '''
    user = update.effective_user
    UsersData.check_user(user)
    UsersData.edit_stage(user, "Wait_voice")
    update.message.reply_text(templates.message_topics)


def voice_block(update: Update, context: CallbackContext) -> None:
    '''
    Главная логика бота при работе с голосовыми сообщениями.

    Args:
        update (Update)
        context (CallbackContext)

    1) Если "stage" пользователя не в ожидаемых ("New") -> пришлем ошибку
    2) Если длительность голосового сообщения не укладывается в интервал
    от MIN_DUR до MAX_DUR -> вернём соответствующее сообщение.
    3) Если всё хорошо -> перешлем пользователю его гс обратно, а также его
    шаблон
    '''
    user = update.effective_user
    user_stage = UsersData.get_stage(user)
    user_template = UsersData.get_template(user)
    voice_obj = update.message.voice

    if user_stage not in ["Wait_template", "Wait_voice"]:
        update.message.reply_text(templates.message_voice_error,
                                  reply_markup=templates.start_markup)
        return

    if voice_obj.duration < templates.MIN_DUR:
        update.message.reply_text(templates.message_short_voice)
    elif voice_obj.duration > templates.MAX_DUR:
        update.message.reply_text(templates.message_long_voice)
    else:
        UsersData.edit_stage(user, 'Wait_template')
        update.message.reply_text("У Вас красивый голос! Давайте прослушаем!")
        update.message.reply_voice(update.message.voice)
        update.message.reply_text(f"Ваш шаблон: {user_template}")
        update.message.reply_text("Пришлите новый шаблон!")

        audio = voice_obj.get_file().download_as_bytearray()
        send_task2(audio, user.id)

async def send_task2(audio, user_id) -> None:

    file_name = f"audio-{dt.datetime.now()}.wav"
    audio_path = os.path.join(path_voice, file_name)

    # @TODO: process I/O exception?
    with open(audio_path, 'wb') as f:
        f.write(audio)

    msg = {"file_name": file_name, "user_id": user_id}

    connection = await connect_robust(host=RABBIT_URL, port=RABBIT_PORT,
                                      client_properties={"connection_name": "caller"})

    async with connection:
        # Creating channel
        channel = await connection.channel()
        rpc = await RPC.create(channel)

        # Creates tasks by proxy object
        #for i in range(1000):
        #    print(await rpc.proxy.multiply(x=100, y=i))

        # Or using create_task method
        await rpc.call("process_audio", kwargs={"file_name": file_name, "user_id": user_id})
        #for i in range(1000):
        #    print(await rpc.call("multiply", kwargs=dict(x=100, y=i)))

        #"amqp://guest:guest@127.0.0.1/",


def send_task(audio, user_id):
    file_name = f"audio-{dt.datetime.now()}.wav"
    audio_path = os.path.join(path_voice, file_name)

    # @TODO: process I/O exception?
    with open(audio_path, 'wb') as f:
        f.write(audio)

    msg = {"file_name": file_name, "user_id": user_id}
    conn_params = pika.ConnectionParameters(host=RABBIT_URL, port=RABBIT_PORT)
    conn = pika.BlockingConnection(conn_params)
    channel = conn.channel()
    channel.queue_declare(queue="voice")
    channel.basic_publish(exchange="", routing_key="voice", body=json.dumps(msg))
    conn.close()


def main() -> None:

    dispatcher.add_handler(CommandHandler("start", start_block))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          main_block))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_block))


    #loop = asyncio.get_event_loop()
    #loop.create_task(get_audio())

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
