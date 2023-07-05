from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap


@app.route('/api/id/', methods=('POST',))
def add_short_link():
    """Функция для создания короткой ссылки через api."""
    return jsonify(
        URLMap().create(db, request.get_json()).to_dict()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_url(short_id):
    """
    Функция для получения оригинальной ссылки через api с помощью short_id.
    """
    return jsonify(url=URLMap.get_original_link(short_id)), HTTPStatus.OK
