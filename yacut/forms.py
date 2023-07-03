from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .settings import LINK_SIZE_MAX, LINK_SIZE_MIN


class YaCutForm(FlaskForm):
    """Класс для создания формы."""
    original_link = URLField(
        label='Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(LINK_SIZE_MIN, LINK_SIZE_MAX)]
    )
    custom_id = StringField(
        label='Ваш вариант короткой ссылки',
        validators=[Length(max=LINK_SIZE_MAX), Optional()]
    )
    submit = SubmitField('Создать')
