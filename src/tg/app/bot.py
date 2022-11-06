import logging
import os
import datetime as dt

from telegram import Update,  ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters, CallbackContext

from classes import Users
import templates


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

UsersData = Users()

path_voice = "/voice/"
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
        audio_path = f'{path_voice}/audio-{dt.datetime.now()}.wav'

        with open(audio_path, 'wb') as f:
            f.write(audio)


def main() -> None:
    updater = Updater(os.environ.get('TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_block))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          main_block))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_block))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
