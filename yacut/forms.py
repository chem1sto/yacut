from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, InputRequired, Length, Optional, Regexp,
                                ValidationError)

from .models import URLMap
from .settings import SHORT_MAX_LENGTH, PATTERN

CUSTOM_ID_EXISTING_ERROR_MESSAGE = 'Имя {custom_id} уже занято!'
CUSTOM_ID_INVALID_SYMBOLS_MESSAGE = (
    '''
    В поле для короткой ссылки введены недопустимые символы.
    Разрешены следующие символы:
    - большие латинские буквы,
    - маленькие латинские буквы,
    - цифры в диапазоне от 0 до 9
    '''
)
CUSTOM_ID_LINK_LABEL = 'Ваш вариант короткой ссылки'
CUSTOM_ID_MAX_LENGTH_MESSAGE = (
    'Длина короткой ссылки не может быть длиннее %(max)d символов'
)
TO_CREATE = 'Создать'
INVALID_LINK_FORMAT = 'Неверный формат адреса ссылки'
OBLIGITARY_FIELD = 'Обязательное поле'
OPTIONAL_FIELD = 'Необязательное поле'
ORIGINAL_LINK_LABEL = 'Длинная ссылка'
ORIGINAL_LINK_MAX_LENGTH_MESSAGE = (
    'Длина оригинальной ссылки не может быть длиннее %(max)d символов'
)


class YaCutForm(FlaskForm):
    """Класс для создания формы YaCutForm."""
    original_link = URLField(
        label=ORIGINAL_LINK_LABEL,
        validators=[
            InputRequired(message=OBLIGITARY_FIELD),
            URL(message=INVALID_LINK_FORMAT)
        ]
    )
    custom_id = StringField(
        description=OPTIONAL_FIELD,
        label=CUSTOM_ID_LINK_LABEL,
        validators=[
            Length(
                max=SHORT_MAX_LENGTH,
                message=CUSTOM_ID_MAX_LENGTH_MESSAGE
            ),
            Regexp(PATTERN, message=CUSTOM_ID_INVALID_SYMBOLS_MESSAGE),
            Optional()
        ]
    )
    submit = SubmitField(TO_CREATE)

    def validate_custom_id(form, custom_id_field):
        """
        Метод экземпляра класса YaCut
        для проверки наличия в БД полученного custom_id.
        """
        if URLMap.query.filter_by(short=custom_id_field.data).first():
            raise ValidationError(CUSTOM_ID_EXISTING_ERROR_MESSAGE.format(
                custom_id=custom_id_field.data
            ))
