from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import YaCutForm
from .models import URLMap
from .settings import BASE_URL, MAIN_PAGE
from .utils import get_unique_short_id, get_urlmap_to_form

FLASH_MESSAGE_CATEGORY = 'url'
TEXT_TO_FLASH_FOR_EXISTING_URL = 'Короткая ссылка для данного URL:'
TEXT_TO_FLASH_FOR_SHORT_URL = 'Ваша новая ссылка готова:'
TEXT_TO_FLASH_TOO_LONG_MESSAGE_ERROR = (
    'Разрешенная длина короткой ссылки 16 символов.'
    'Длинна вашей короткой ссылки {length} символов'
)
TEXT_TO_FLASH_EXISTING_SHORT_NAME_MESSAGE_ERROR = (
    'Имя {short_name} уже занято!'
)


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
    short_link = form.custom_id.data
    if URLMap.query.filter_by(short=short_link).first():
        flash(TEXT_TO_FLASH_EXISTING_SHORT_NAME_MESSAGE_ERROR.format(
            short_name=short_link
        ))
        form.custom_id.data = None
        return render_template(MAIN_PAGE, form=form)
    if short_link is None or short_link == '':
        form.custom_id.data = get_unique_short_id()
    if len(form.custom_id.data) > 16:
        flash(TEXT_TO_FLASH_TOO_LONG_MESSAGE_ERROR.format(
            length=len(form.custom_id.data)
        ))
        form.custom_id.data = None
        return render_template(MAIN_PAGE, form=form)
    if get_urlmap_to_form(form=form) is not None:
        flash(TEXT_TO_FLASH_FOR_EXISTING_URL)
        flash(
            f'{BASE_URL}/{form.custom_id.data}', FLASH_MESSAGE_CATEGORY
        )
        return render_template(MAIN_PAGE, form=form)
    db.session.add(
        URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
    )
    db.session.commit()
    flash(TEXT_TO_FLASH_FOR_SHORT_URL)
    flash(
        f'{BASE_URL}/{get_urlmap_to_form(form).short}',
        FLASH_MESSAGE_CATEGORY
    )
    return render_template(MAIN_PAGE, form=form)


@app.route('/<string:short>')
def redirection_view(short):
    """View-функция для переадресации пользователя по короткой ссылке."""
    urlmap = URLMap.query.filter_by(short=short).one_or_none()
    if urlmap is not None:
        return redirect(urlmap.original)
    abort(HTTPStatus.NOT_FOUND)
