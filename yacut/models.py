from datetime import datetime as dt
from random import choice
from re import findall

from flask import url_for
from validators import url

from . import db
from .exceptions import ExistingShortLinkError, InvalidOriginalLinkError
from .settings import (
    ALLOWED_SYMBOLS, API_ORIGINAL, API_SHORT,
    ORIGINAL_SIZE_MAX, PATTERN, REDIRECTION_VIEW,
    REPEAT_TIMES, SHORT_AUTO_LENGTH, SHORT_MAX_LENGTH
)

ORIGINAL_VALUE_ERROR_MESSAGE = (
    '{original} не является корректной url-ссылкой.'
)

SHORT_VALUE_ERROR_MESSAGE = (
    'Короткая ссылка {short} слишком длинная или содержит недопустимые символы.'
)
LOOKUP_ERROR_MESSAGE = (
    'Короткая ссылка {short} уже есть в базе данных.'
)


class URLMap(db.Model):
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
        return (
            f'id: {self.id}'
            f'original: {self.original}'
            f'short: {self.short}'
            f'timestamp: {self.timestamp}'
        )

    def to_dict(self):
        """Вывод информации о конкретном экземпляре класса URLMap
        в виде словаря."""
        return {
            API_ORIGINAL: self.original,
            API_SHORT: url_for(
                REDIRECTION_VIEW, short=self.short, _external=True
            )
        }

    def create(original, short, raw_data=False):
        """
        Создания новой записи в БД:
        - При отсутвии короткой ссылки - вызов функции для её генерации;
        - При получении raw_data - валидация полученных данных.
        """
        if raw_data and short:
            if not url(original):
                raise InvalidOriginalLinkError(
                    ORIGINAL_VALUE_ERROR_MESSAGE.format(
                        original=original
                    )
                )
            if (
                len(short) > SHORT_MAX_LENGTH or
                not bool(findall(PATTERN, short))
            ):
                raise ValueError(SHORT_VALUE_ERROR_MESSAGE.format(
                    short=short
                ))
            if URLMap.get(short):
                raise ExistingShortLinkError(LOOKUP_ERROR_MESSAGE.format(
                    short=short
                ))
        if not short:
            short = URLMap.get_unique_short_id()
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
        Получение экземпляра класса по короткой ссылке.
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        """
        Генерация уникальной короткой ссылки.
        """
        for time in range(REPEAT_TIMES):
            short = ''.join(choice(
                ALLOWED_SYMBOLS) for _ in range(SHORT_AUTO_LENGTH))
            if URLMap.get(short) is None:
                return short
