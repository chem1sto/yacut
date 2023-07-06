from datetime import datetime as dt

from random import choice
from re import findall

from flask import url_for

from . import db
from .settings import (
    ALLOWED_SYMBOLS, API_ORIGINAL, API_SHORT,
    ORIGINAL_SIZE_MAX, PATTERN, REDIRECTION_VIEW,
    SHORT_AUTO_LENGTH, SHORT_MAX_LENGTH
)

EXISTING_SHORT_ID_ERROR_MESSAGE = 'Имя "{short}" уже занято.'
INVALID_SHORT_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)


class URLMap(db.Model):
    """Класс для создания модели URLMap."""
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(ORIGINAL_SIZE_MAX),
        nullable=False
    )
    short = db.Column(
        db.String(SHORT_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True
    )
    timestamp = db.Column(
        db.DateTime,
        default=dt.utcnow
    )

    def __repr__(self) -> str:
        """Магический метод удобного для чтения человеком
        представления класса URLMap."""
        return (
            f'id: {self.id}'
            f'original: {self.original}'
            f'short: {self.short}'
            f'timestamp: {self.timestamp}'
        )

    def to_dict(self):
        """Метод экземпляра класса URLMap для вывода информации
        о конкретном экземпляре класса URLMap в виде словаря."""
        return {
            API_ORIGINAL: self.original,
            API_SHORT: url_for(
                REDIRECTION_VIEW, short=self.short, _external=True
            )
        }

    def create(original, short):
        """Метод экземпляра класса URLMap для создания новой записи в БД."""
        if not short or short == '' or short is None:
            short = URLMap.get_unique_short_id()
        if (
            len(short) > SHORT_MAX_LENGTH or
            not bool(findall(PATTERN, short))
        ):
            raise ValueError
        if URLMap.get(short):
            raise LookupError
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        """
        Метод класса URLMap для проверки наличия короткой ссылки в БД.
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        """
        Статический метод класса URLMap
        для генерации уникальной короткой ссылки.
        """
        short = ''.join(choice(
            ALLOWED_SYMBOLS) for _ in range(SHORT_AUTO_LENGTH))
        if URLMap.get(short) is None:
            return short
        return URLMap.get_unique_short_id()
