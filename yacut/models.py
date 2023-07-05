from datetime import datetime as dt
from random import sample
from http import HTTPStatus

from . import db
from .exceptions import InvalidAPIUsage
from .settings import (ALPHABET, API_ORIGINAL, API_SHORT, BASE_URL,
                       CUSTOM_ID_AUTO_LENGTH, CUSTOM_ID_MAX_LENGTH,
                       LINK_SIZE_MAX, ORIGINAL, PATTERN, SHORT)
from .utils import get_invalid_symbols

INVALID_CUSTOM_ID_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
EMPTY_ERROR_MESSAGE = 'Отсутствует тело запроса'
EXISTING_SHORT_ID_ERROR_MESSAGE = 'Имя "{short_id}" уже занято.'
NO_ID_ERROR_MESSAGE = 'Указанный id не найден'
NO_URL_ERROR_MESSAGE = '"url" является обязательным полем!'


class Model_PK(db.Model):
    """Абстрактный класс-для создания поля id в модели URLMap"""
    __abstract__ = True
    id = db.Column(
        db.Integer,
        primary_key=True
    )


class TimestampMixin:
    """Класс-миксин для создания поля timestamp в модели URLMap"""
    timestamp = db.Column(
        db.DateTime,
        default=dt.utcnow
    )


class URLMap(Model_PK, TimestampMixin):
    """Класс для создания модели URLMap."""
    original = db.Column(
        db.String(CUSTOM_ID_MAX_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(LINK_SIZE_MAX),
        unique=True,
        nullable=False,
        index=True
    )

    def __repr__(self) -> str:
        """Магический метод для формального представления класса URLMap."""
        return (
            f'id: {self.id}\n'
            f'original: {self.original}\n'
            f'short: {self.short}\n'
            f'timestamp: {self.timestamp}\n'
        )

    @classmethod
    def get_original_link(cls, short_id):
        """
        Метод класса URLMap для получения оригинальной ссылки
        по её короткой ассоциации.
        """
        url_map = cls.query.filter_by(short=short_id).one_or_none()
        if url_map is None:
            raise InvalidAPIUsage(NO_ID_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
        return url_map.original

    @classmethod
    def check_custom_id_existing(cls, custom_id):
        """
        Метод класса URLMap для проверки наличия короткой ссылки в БД."""
        return bool(cls.query.filter_by(short=custom_id).first())

    @classmethod
    def clean_data(cls, data):
        """
        Метод класса URLMap для проверки и при необходимости
        дополнения полученных данных.
        """
        if not data:
            raise InvalidAPIUsage(EMPTY_ERROR_MESSAGE)
        original, short = data.get(API_ORIGINAL), data.get(SHORT)
        if not original:
            raise InvalidAPIUsage(USAGE_NO_URL_ERROR_MESSAGE)
        if not short:
            short = URLMap.get_unique_short_id(URLMap, cls.short)
        elif (
            len(short) > CUSTOM_ID_MAX_LENGTH or
            get_invalid_symbols(PATTERN, short)
        ):
            raise InvalidAPIUsage(INVALID_CUSTOM_ID_ERROR_MESSAGE)
        elif URLMap.query.filter(cls.short == short).count():
            raise InvalidAPIUsage(EXISTING_SHORT_ID_ERROR_MESSAGE.format(
                short_id=short
            ))
        return original, short

    def to_internal_value(self, data, api):
        """
        Метод экземпляра класса URLMap для обработки и вывода полученных данных.
        """
        if api:
            self.original, self.short = self.__class__.clean_data(data)
        else:
            self.original, self.short = data.get(ORIGINAL), data.get(SHORT)
        return self

    def to_dict(self):
        """Метод экземпляра класса URLMap для вывода информации
        о конкретном экземпляре класса URLMap в виде словаря."""
        return {
            API_ORIGINAL: self.original,
            API_SHORT: f'{BASE_URL}/{self.short}',
        }

    def create(self, db, data, api=True):
        """Метод экземпляра класса URLMap для создания новой записи в БД."""
        db.session.add(self.to_internal_value(data, api))
        db.session.commit()
        return self

    @staticmethod
    def get_unique_short_id(cls, field):
        """
        Статический метод класса URLMap
        для генерации уникальной короткой ссылки.
        """
        short_id = ''.join(sample(ALPHABET, CUSTOM_ID_AUTO_LENGTH))
        while cls.query.filter(field == short_id).count():
            short_id = ''.join(sample(ALPHABET, CUSTOM_ID_AUTO_LENGTH))
        return short_id
