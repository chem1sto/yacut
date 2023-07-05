from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, InputRequired, Length, Optional,
                                ValidationError)

from .models import URLMap
from .settings import CUSTOM_ID_MAX_LENGTH, LINK_SIZE_MAX, PATTERN
from .utils import get_invalid_symbols

CUSTOM_ID_EXISTING_ERROR_MESSAGE = 'Имя {custom_id} уже занято!'
CUSTOM_ID_INVALID_SYMBOLS_MESSAGE = (
    'В поле для короткой ссылки введены недопустимые символы {invalid_symbols}')
CUSTOM_ID_LINK_LABEL = 'Ваш вариант короткой ссылки'
CUSTOM_ID_MAX_LENGTH_MESSAGE = (
    'Длина короткой ссылки не может быть длиннее %(max)d символов'
)
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
            Length(max=LINK_SIZE_MAX, message=ORIGINAL_LINK_MAX_LENGTH_MESSAGE),
            URL(message=INVALID_LINK_FORMAT)
        ]
    )
    custom_id = StringField(
        description=OPTIONAL_FIELD,
        label=CUSTOM_ID_LINK_LABEL,
        validators=[
            Length(
                max=CUSTOM_ID_MAX_LENGTH,
                message=CUSTOM_ID_MAX_LENGTH_MESSAGE),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, custom_id_field):
        """
        Метод экземпляра класса YaCut
        для проверки наличия в БД полученного custom_id.
        """
        if not custom_id_field.data:
            return None
        invalid_symbols = get_invalid_symbols(PATTERN, custom_id_field.data)
        if invalid_symbols:
            raise ValidationError(
                CUSTOM_ID_INVALID_SYMBOLS_MESSAGE.format(
                    invalid_symbols=invalid_symbols
                )
            )
        if URLMap.check_custom_id_existing(custom_id_field.data):
            raise ValidationError(CUSTOM_ID_EXISTING_ERROR_MESSAGE.format(
                custom_id=custom_id_field.data
            ))
