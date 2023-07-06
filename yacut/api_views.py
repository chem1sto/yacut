from http import HTTPStatus
from re import findall

from flask import jsonify, request

from . import app
from .exceptions import InvalidAPIUsage
from .models import URLMap
from .settings import API_ORIGINAL, PATTERN, SHORT, SHORT_MAX_LENGTH

EMPTY_ERROR_MESSAGE = 'Отсутствует тело запроса'
EXISTING_SHORT_ID_ERROR_MESSAGE = 'Имя "{short}" уже занято.'
NO_ID_ERROR_MESSAGE = 'Указанный id не найден'
NO_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
INVALID_SHORT_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)


@app.route('/api/id/', methods=('POST',))
def add_short_link():
    """Функция для создания короткой ссылки через api."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_ERROR_MESSAGE)
    if API_ORIGINAL not in data:
        raise InvalidAPIUsage(NO_URL_ERROR_MESSAGE)
    if SHORT not in data or data[SHORT] == '' or data[SHORT] is None:
        data[SHORT] = URLMap.get_unique_short_id()
    short = data.get(SHORT)
    if (
        len(short) > SHORT_MAX_LENGTH or
        not bool(findall(PATTERN, short))
    ):
        raise InvalidAPIUsage(INVALID_SHORT_ERROR_MESSAGE)
    if URLMap.get(short):
        raise InvalidAPIUsage(EXISTING_SHORT_ID_ERROR_MESSAGE.format(
            short=short
        ))
    return jsonify(
        URLMap.create(
            original=data.get(API_ORIGINAL),
            short=data.get(SHORT)
        ).to_dict()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=('GET',))
def get_original(short):
    """
    Функция для получения оригинальной ссылки через api с помощью short_id.
    """
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(NO_ID_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify(url=url_map.original), HTTPStatus.OK
