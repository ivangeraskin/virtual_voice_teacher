from telegram import ReplyKeyboardMarkup


MIN_DUR = 3
MAX_DUR = 10

start_markup = ReplyKeyboardMarkup([['Шаблон']],
                                    one_time_keyboard=True,
                                    resize_keyboard=True,
                                  )

cancel_markup = ReplyKeyboardMarkup([['Отмена']],
                                    one_time_keyboard=True,
                                    resize_keyboard=True,
                                  )

template_text = "Говорил командир про полковника и про полковницу, про подполковника и про подполковницу, про поручика и про поручицу, про подпоручика и про подпоручицу, про прапорщика и про прапорщицу, про подпрапорщика, а про подпрапорщицу молчал."

message_change_template = "Жду Ваше голосовое!\nВы можете поменять шаблон, прислав его сюда повторно.\nЕсли Вас устраивает шаблон, то пришлите голосовое сообщение"

message_greeting = f"Моё имя <b>Voice Teacher</b>, я помогаю поставить речь.\nПришлите, пожалуйста, текст, который собираетесь озвучить,\nили выберите кнопку <b>шаблон</b> (тогда я вышлю текст, который нужно будет озвучить)\nУчтите, голосовое сообщение должно быть от {MIN_DUR} до {MAX_DUR} секунд!"

message_get_template = "Пожалуйста, отправьте голосовое, где Вы озвучиваете этот текст!"

message_voice_wait = "Спасибо! Пожалуйста, озвучьте Ваш текст"

message_short_voice = "Голосовое точно записалось? Попробуйте ещё раз"

message_long_voice = "Длинное голосовое сообщение.."

message_voice_error = "Пожалуйста, пришлите свой шаблон или выберите наш шаблон"

message_not_found_user = 'Пожалуйста, нажмите сначала на "start"'
