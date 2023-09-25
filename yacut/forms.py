from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from .constants import MAX_CUSTOM_ID, MIN_LEN_LINK

class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(min=MIN_LEN_LINK)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                min=MIN_LEN_LINK, max=MAX_CUSTOM_ID,
                message='Максимальная длина 16 символов'
            ),
            Optional()
        ]
    )

    submit = SubmitField('Создать')
