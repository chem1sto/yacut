from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .settings import API_ORIGINAL, API_SHORT, BASE_URL
from .utils import get_unique_short_id, validate_short_id

INVALID_API_USAGE_EMPTY_ERROR_MESSAGE = 'Отсутствует тело запроса'
INVALID_API_USAGE_NO_URL_ERROR_MESSAGE = '"url" является обязательным полем!'
INVALID_API_USAGE_NO_ID_ERROR_MESSAGE = 'Указанный id не найден'
INVALID_API_USAGE_TOO_LONG_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)
INVALID_API_USAGE_EXISTING_SHORT_ID_ERROR_MESSAGE = (
    'Имя "{short_id}" уже занято.'
)
INVALID_API_USAGE_FORBIDDEN_SYMBOLS_ERROR_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)


@app.route('/api/id/', methods=('POST',))
def add_short_link():
    """Функция для создания короткой ссылки через api."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(INVALID_API_USAGE_EMPTY_ERROR_MESSAGE)
    if API_ORIGINAL not in data:
        raise InvalidAPIUsage(INVALID_API_USAGE_NO_URL_ERROR_MESSAGE)
    if (
        API_SHORT not in data or
        data[API_SHORT] == '' or
        data[API_SHORT] is None
    ):
        short_id = get_unique_short_id()
    else:
        short_id = data[API_SHORT]
    if len(short_id) > 16:
        raise InvalidAPIUsage(
            INVALID_API_USAGE_TOO_LONG_ERROR_MESSAGE.format(
                length=len(short_id)
            )
        )
    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage(
            INVALID_API_USAGE_EXISTING_SHORT_ID_ERROR_MESSAGE.format(
                short_id=short_id
            )
        )
    if validate_short_id(short_id):
        urlmap = URLMap()
        data['original'] = data['url']
        data['short'] = short_id
        urlmap.from_dict(data)
        db.session.add(urlmap)
        db.session.commit()
        return jsonify(
            url=urlmap.original,
            short_link=f'{BASE_URL}/{urlmap.short}'
        ), HTTPStatus.CREATED
    else:
        raise InvalidAPIUsage(
            INVALID_API_USAGE_FORBIDDEN_SYMBOLS_ERROR_MESSAGE
        )


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_url(short_id):
    """
    Функция для получения оригинальной ссылки через api с помощью short_id.
    """
    urlmap = URLMap.query.filter_by(short=short_id).one_or_none()
    if urlmap is None:
        raise InvalidAPIUsage(
            INVALID_API_USAGE_NO_ID_ERROR_MESSAGE.format(short_id=short_id),
            HTTPStatus.NOT_FOUND
        )
    return jsonify(url=urlmap.original), HTTPStatus.OK
