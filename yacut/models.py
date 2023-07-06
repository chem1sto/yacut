from datetime import datetime as dt
from random import sample

from flask import url_for

from . import db
from .settings import (ALPHABET, API_ORIGINAL, API_SHORT, ORIGINAL_SIZE_MAX,
                       REDIRECTION_VIEW, REPEAT, SHORT_AUTO_LENGTH,
                       SHORT_MAX_LENGTH)


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
            API_SHORT: url_for(
                REDIRECTION_VIEW, short=self.short, _external=True
            )
        }

    def create(original, short):
        """Метод экземпляра класса URLMap для создания новой записи в БД."""
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
        Метод класса URLMap для получения оригинальной ссылки
        по её короткой ассоциации.
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        """
        Статический метод класса URLMap
        для генерации уникальной короткой ссылки.
        """
        for _ in range(REPEAT):
            short = ''.join(sample(ALPHABET, SHORT_AUTO_LENGTH))
            if not URLMap.get(short):
                break
        return short
