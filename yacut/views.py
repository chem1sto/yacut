from flask import flash, redirect, render_template

from . import app, db
from .forms import YaCutForm
from .models import URLMap
from .settings import MAIN_PAGE

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
        form.custom_id.data = None
        return render_template(MAIN_PAGE, form=form)
    if not form.custom_id.data:
        form.custom_id.data = URLMap.get_unique_short_id(URLMap, URLMap.short)
    URLMap().create(db, form.data, api=False).short
    flash(SHORT_LINK_IS_READY)
    return render_template(MAIN_PAGE, form=form)


@app.route('/<string:short>')
def redirection_view(short):
    """View-функция для переадресации пользователя по короткой ссылке."""
    return redirect(URLMap.get_original_link(short))
