from flask import abort, redirect, render_template, url_for
from http import HTTPStatus

from . import app
from .forms import YaCutForm
from .models import URLMap
from .settings import MAIN_PAGE, REDIRECTION_VIEW
from .exceptions import InvalidFormUsage

SHORT_LINK_IS_READY = 'Ваша новая ссылка готова:'
ERROR_MESSAGE = 'Что-то пошло не так: {errors}'


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """
    View-функция для работы главной страницы:
    - Проверка введенных в форму данных;
    - Создание новой короткой ссылки для введенной оригинальной ссылки;
    - Вывод возможных ошибок.
    """
    form = YaCutForm()
    if not form.validate_on_submit():
        return render_template(MAIN_PAGE, form=form)
    try:
        return render_template(
            MAIN_PAGE,
            form=form,
            url=url_for(
                REDIRECTION_VIEW,
                short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data
                ).short,
                _external=True
            )
        )
    except (TypeError, ValueError) as errors:
        raise InvalidFormUsage(ERROR_MESSAGE.format(errors=errors))


@app.route('/<string:short>')
def redirection_view(short):
    """View-функция для переадресации пользователя по короткой ссылке."""
    url_map = URLMap.get(short)
    if url_map is not None:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
