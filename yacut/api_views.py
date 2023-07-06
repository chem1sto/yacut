from http import HTTPStatus

from flask import jsonify, request

from . import app
from .exceptions import InvalidAPIUsage
from .models import URLMap
from .settings import API_ORIGINAL, NO_URL_ERROR_MESSAGE, SHORT

EMPTY_ERROR_MESSAGE = 'Отсутствует тело запроса'
NO_ID_ERROR_MESSAGE = 'Указанный id не найден'


@app.route('/api/id/', methods=('POST',))
def add_short_link():
    """Функция для создания короткой ссылки через api."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(EMPTY_ERROR_MESSAGE)
    if API_ORIGINAL in data:
        original, short = data.get(API_ORIGINAL), data.get(SHORT)
        return jsonify(
            URLMap.create(
                URLMap,
                original=original,
                short=short
            ).to_dict()
        ), HTTPStatus.CREATED
    raise InvalidAPIUsage(NO_URL_ERROR_MESSAGE)


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_url(short_id):
    """
    Функция для получения оригинальной ссылки через api с помощью short_id.
    """
    url_map = URLMap.get(URLMap, short_id)
    if url_map is None:
        raise InvalidAPIUsage(NO_ID_ERROR_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify(url=url_map.original), HTTPStatus.OK
