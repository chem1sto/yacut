from re import findall
from random import choice
from string import ascii_letters, digits

from .models import URLMap
from .settings import CUSTOM_ID_AUTO_LENGTH, PATTERN


ALPHABET = ascii_letters + digits


def get_urlmap_to_form(form):
    """Функция для получения объекта URLMap для формы."""
    return URLMap.query.filter_by(
        original=form.original_link.data
    ).one_or_none()


def get_unique_short_id():
    """Функция для генерации уникальной короткой ссылки."""
    short = ''.join(choice(ALPHABET) for _ in range(CUSTOM_ID_AUTO_LENGTH))
    return short


def validate_short_id(short_id):
    """Функция для проверки введённых символов для short_id."""
    authorized_symbols_in_short_id = findall(PATTERN, short_id)
    return ''.join(authorized_symbols_in_short_id) == short_id
