from datetime import datetime
import logging

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, create_engine, distinct, BigInteger
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import func
import os

from typing import Dict, List

Base = declarative_base()
_logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    create_dt = Column(DateTime(timezone=True), server_default=func.now())
    reactions = relationship("Reaction")


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, "user.id")
    file_id = Column(String)
    score = Column(Integer)
    comments = Column(String)
    create_dt = Column(DateTime(timezone=True), server_default=func.now())


class DBDriver:

    def __init__(self):
        self._engine = create_engine(self._database_url)
        self._sm = sessionmaker(bind=self._engine)
        self._database_url = self._get_db_url()
        Base.metadata.create_all(self._engine)

    def _get_db_url(self):
        """
        Evaluates path to the db
        :return:
        """
        _DB_NAME = os.environ.get("DB_NAME")
        _DB_ADDRESS = os.environ.get("DB_ADDRESS")
        _DB_PORT = os.environ.get("DB_PORT")
        _DB_USER = os.environ.get("DB_USER")
        _DB_PASSWORD = os.environ.get("DB_PASSWORD")
        return f"postgresql://{_DB_USER}:{_DB_PASSWORD}@{_DB_ADDRESS}:{_DB_PORT}/{_DB_NAME}"

    def add_user(self, user: Dict):
        """
        Add user to the db
        :param user:
        :return:
        """
        new_user = User(
            tg_id=int(user["tg_id"])
        )

        with self._sm() as session:
            session.add(new_user)
            session.commit()
            session.close()

    def add_review(self, reaction: Dict):
        """
        Add user reaction

        :param reaction:
        :return:
        """
        session = self._sm()
        user_id = session.query(User.id) \
                         .filter(User.tg_id == reaction["tg_id"]) \
                         .first()

        if user_id is None:
            _logger.warning("User with Tg ID %s is not found.", repr(reaction["tg_id"]))
            session.close()
            return None

        user_id = user_id[0]

        review = Review(user_id=user_id,
                        score=reaction["score"])
        session.add(review)
        session.commit()
        session.close()