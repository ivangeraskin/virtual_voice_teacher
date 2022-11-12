import datetime as dt
from telegram import Update

from dataclasses import dataclass, field
from typing import Union


@dataclass
class User:
    '''
    Класс (структура) пользователя.

    Args:
        user_id (int): id пользователя в telegram
        stage (str): на каком этапе пользователь находится в данный момент:
          1) "New" - зарегистрирован
          2) "Wait_template" - ждем от него шаблон текста
          3) "Wait_voice" - ждем от него голосовое сообщение
        template (str): шаблон, который пользователь озвучивает
        born (datetime.datetime): дата регистрации в боте
    '''
    user_id: int
    stage: str = "New"
    template: str = ""
    born: dt.datetime = field(default_factory=dt.datetime.now)


class Users:
    '''
    Класс пользователей.

    Args:
        __users (dict of int: User): User'ы

    Attributes:
        __users (dict of int: User): User'ы
    '''
    def __init__(self) -> None:
        self.__users = {}

    def __add_user(self, user: Update.effective_user):
        """
        Добавить пользователя
        """
        user_id = user.id
        self.__users[user_id] = User(user_id=user_id)

    def __get_user(self, user: Update.effective_user, return_user=False) -> Union[User, bool]:
        """
        Получить пользователя из __users.
        Если return_user=True то вернет пользователя из __users.
        Иначе bool (есть/нет)
        """
        user_id = user.id
        if user_id not in self.__users:
            return False
        elif return_user:
            return self.__users[user_id]
        return True

    def check_user(self, user: Update.effective_user) -> None:
        """
        Проверить пользователя в __users.
        Если его нет, то добавить в __users.
        """
        if not self.__get_user(user):
            self.__add_user(user)

    def get_stage(self, user: Update.effective_user) -> str:
        """
        Получить stage пользователя
        """
        return self.__users[user.id].stage

    def get_template(self, user: Update.effective_user) -> str:
        """
        Получить template пользователя
        """
        return self.__users[user.id].template

    def edit_stage(self, user: Update.effective_user, new_stage: str) -> None:
        """
        Изменить stage пользователя
        """
        self.__users[user.id].stage = new_stage

    def edit_template(self, user: Update.effective_user, new_template: str) -> None:
        """
        Изменить template пользователя
        """
        self.__users[user.id].template = new_template
