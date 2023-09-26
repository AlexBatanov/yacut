import re

from .models import URLMap

from . import app
app.logger.info('validators')
from .constants import DATA_NOT, MAX_CUSTOM_ID, NOT_CORRECT_NAME_LINK, REQUERED_URL_FIELD, name_is_ocuppet
from .error_handlers import InvalidAPIUsage

def url_validator_in_data(data: dict):
    """
    Проверяет данные запроса API на валидность.
    """
    if not data:
        raise InvalidAPIUsage(DATA_NOT)
    if 'url' not in data:
        raise InvalidAPIUsage(REQUERED_URL_FIELD)


def is_english_alphanumeric(input_string: str):
    """
    Проверяет, состоит ли входная строка только из латинских букв и цифр.
    """
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, input_string))


def validator_custom_id(custom_id):
    """
    Проверяет, кастомную ссылку на валидность.
    """
    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(name_is_ocuppet(custom_id, api=True))
    if (len(custom_id) > MAX_CUSTOM_ID or
        not is_english_alphanumeric(custom_id)):
        raise InvalidAPIUsage(NOT_CORRECT_NAME_LINK)
    
