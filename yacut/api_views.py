from http import HTTPStatus

from flask import jsonify, request

from . import app
from .exceptions import (ExistingShortLinkError, InvalidAPIUsage,
                         InvalidOriginalLinkError)
from .models import URLMap
from .settings import API_ORIGINAL, SHORT

EXISTING_SHORT_ID_ERROR_MESSAGE = 'Имя "{short}" уже занято.'
EMPTY_ERROR_MESSAGE = 'Отсутствует тело запроса'
INVALID_ORIGINAL_ERROR_MESSAGE = (
    'Указано недопустимое имя для оригинальной ссылки'
)
INVALID_SHORT_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
NO_ID_ERROR_MESSAGE = 'Указанный id не найден'
NO_URL_ERROR_MESSAGE = '"url" является обязательным полем!'


@app.route('/api/id/', methods=('POST',))
def add_short_link():
    """Функция для создания короткой ссылки через api."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_ERROR_MESSAGE)
    if API_ORIGINAL not in data:
        raise InvalidAPIUsage(NO_URL_ERROR_MESSAGE)
    try:
        return jsonify(
            URLMap.create(
                original=data.get(API_ORIGINAL),
                short=data.get(SHORT),
                raw_data=True
            ).to_dict()
        ), HTTPStatus.CREATED
    except InvalidOriginalLinkError:
        raise InvalidAPIUsage(
            INVALID_ORIGINAL_ERROR_MESSAGE, HTTPStatus.BAD_REQUEST
        )
    except ValueError:
        raise InvalidAPIUsage(
            INVALID_SHORT_ERROR_MESSAGE, HTTPStatus.BAD_REQUEST
        )
    except ExistingShortLinkError:
        raise InvalidAPIUsage(EXISTING_SHORT_ID_ERROR_MESSAGE.format(
            short=data.get(SHORT)
        ), HTTPStatus.BAD_REQUEST)


@app.route('/api/id/<string:short>/', methods=('GET',))
def get_original(short):
    """
    Функция для получения оригинальной ссылки через api с помощью short.
    """
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(NO_ID_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify(url=url_map.original), HTTPStatus.OK
