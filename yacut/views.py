from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .exceptions import InvalidFormUsage
from .forms import YaCutForm
from .models import URLMap
from .settings import MAIN_PAGE, REDIRECTION_VIEW


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
    except (LookupError, ValueError) as errors:
        flash(InvalidFormUsage(errors))
        return render_template(MAIN_PAGE, form=form)


@app.route('/<string:short>')
def redirection_view(short):
    """View-функция для переадресации пользователя по короткой ссылке."""
    url_map = URLMap.get(short)
    if url_map is not None:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
