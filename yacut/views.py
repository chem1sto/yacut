from flask import abort, redirect, render_template, url_for
from http import HTTPStatus

from . import app
from .forms import YaCutForm
from .models import URLMap
from .settings import MAIN_PAGE, REDIRECTION_VIEW

SHORT_LINK_IS_READY = 'Ваша новая ссылка готова:'


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """
    View-функция для работы главной страницы:
    - Проверка введенных в форму данных;
    - Вывод во флеш-сообщении ранее созданной короткой ссылки;
    - Создание новой короткой ссылки для введенной оригинальной ссылки
    - Вывод во флеш-сообщении новой ссылки.
    """
    form = YaCutForm()
    if not form.validate_on_submit():
        return render_template(MAIN_PAGE, form=form)
    try:
        url_map = URLMap.create(
            URLMap,
            original=form.original_link.data,
            short=form.custom_id.data
        )
    except Exception as error:
        raise error
    form.custom_id.data = url_map.short
    return render_template(
        MAIN_PAGE,
        form=form,
        url=url_for(REDIRECTION_VIEW, short=url_map.short, _external=True)
    )


@app.route('/<string:short>')
def redirection_view(short):
    """View-функция для переадресации пользователя по короткой ссылке."""
    url_map = URLMap.get(URLMap, short)
    if url_map is not None:
        return redirect(url_map.original)
    abort(HTTPStatus.NOT_FOUND)
