from datetime import datetime as dt
from random import sample
from re import findall
from urllib.parse import urljoin

from flask import url_for

from . import db
from .exceptions import InvalidAPIUsage
from .settings import (ALPHABET, API_ORIGINAL, API_SHORT,
                       NO_URL_ERROR_MESSAGE, PATTERN, REPEAT, REDIRECTION_VIEW,
                       SHORT_AUTO_LENGTH, SHORT_MAX_LENGTH)

INVALID_CUSTOM_ID_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
EXISTING_SHORT_ID_ERROR_MESSAGE = 'Имя "{short_id}" уже занято.'


class URLMap(db.Model):
    """Класс для создания модели URLMap."""
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String,
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
        """Магический метод для формального представления класса URLMap."""
        return (
            f'id: {self.id}\n'
            f'original: {self.original}\n'
            f'short: {self.short}\n'
            f'timestamp: {self.timestamp}\n'
        )

    def to_dict(self):
        """Метод экземпляра класса URLMap для вывода информации
        о конкретном экземпляре класса URLMap в виде словаря."""
        return {
            API_ORIGINAL: self.original,
            API_SHORT: urljoin(
                url_for(
                    REDIRECTION_VIEW, short=self.short, _external=True
                ), self.short
            )
        }

    def create(self, original, short):
        """Метод экземпляра класса URLMap для создания новой записи в БД."""
        if not original:
            raise InvalidAPIUsage(NO_URL_ERROR_MESSAGE)
        if not short:
            short = URLMap.get_unique_short_id(URLMap, short)
        elif (
            len(short) > SHORT_MAX_LENGTH or
            not bool(findall(PATTERN, short))
        ):
            raise InvalidAPIUsage(INVALID_CUSTOM_ID_ERROR_MESSAGE)
        elif URLMap.query.filter(self.short == short).count():
            raise InvalidAPIUsage(EXISTING_SHORT_ID_ERROR_MESSAGE.format(
                short_id=short
            ))
        url_map = self(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(cls, short_id):
        """
        Метод класса URLMap для получения оригинальной ссылки
        по её короткой ассоциации.
        """
        return cls.query.filter_by(short=short_id).first()

    @staticmethod
    def get_unique_short_id(cls, field):
        """
        Статический метод класса URLMap
        для генерации уникальной короткой ссылки.
        """
        for _ in range(REPEAT):
            short = ''.join(sample(ALPHABET, SHORT_AUTO_LENGTH))
            if not cls.query.filter(field == short).count():
                break
        return short
