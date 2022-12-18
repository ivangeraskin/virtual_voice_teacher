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


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    tg_name = Column(String)
    file_id = Column(String)
    score = Column(Integer, nullable=True)
    comments = Column(String)
    create_dt = Column(DateTime(timezone=True), server_default=func.now())


class DBDriver:

    def __init__(self):
        self._database_url = self._get_db_url()
        self._engine = create_engine(self._database_url)
        self._sm = sessionmaker(bind=self._engine)
        Base.metadata.create_all(self._engine)

    def _get_db_url(self):
        """
        Evaluates path to the db
        :return:
        """
        _DB_NAME = os.environ["DB_NAME"]
        _DB_ADDRESS = os.environ["DB_ADDRESS"]
        _DB_PORT = os.environ["DB_PORT"]
        _DB_USER = os.environ["DB_USER"]
        _DB_PASSWORD = os.environ["DB_PASSWORD"]
        return f"postgresql://{_DB_USER}:{_DB_PASSWORD}@{_DB_ADDRESS}:{_DB_PORT}/{_DB_NAME}"


    def add_review(self, review: Dict):
        """
        Add user reaction

        :param reaction:
        :return:
        """
        session = self._sm()
        params = review.dict()
        if not params.get("score"):
            params["score"] = -1
        review = Review(**params)
        session.add(review)
        try:
            session.commit()
            session.close()
        except Exception as err:
            _logger.error(repr(err))
            return -1
        else:
            return 0