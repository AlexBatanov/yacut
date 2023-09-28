import re

from .models import URLMap
from .error_handlers import InvalidAPIUsage, NotUniqueCustomId
from .constants import (DATA_NOT, MAX_CUSTOM_ID, NOT_CORRECT_NAME_LINK,
                        NOT_UNICUE_CUSTOM_ID, NOT_UNICUE_CUSTOM_ID_API,
                        REQUERED_URL_FIELD, PATTERN)


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
    return bool(re.match(PATTERN, input_string))


def validator_custom_id_api(custom_id):
    """
    Проверяет, кастомную ссылку в апи на валидность.
    """
    if URLMap.is_exists(custom_id):
        raise InvalidAPIUsage(NOT_UNICUE_CUSTOM_ID_API.format(custom_id))
    if (len(custom_id) > MAX_CUSTOM_ID or
            not is_english_alphanumeric(custom_id)):
        raise InvalidAPIUsage(NOT_CORRECT_NAME_LINK)


def validator_custom_id_views(custom_id):
    """
    Проверяет, кастомную ссылку в представлении на валидность.
    """
    if URLMap.is_exists(custom_id):
        raise NotUniqueCustomId(NOT_UNICUE_CUSTOM_ID.format(custom_id))
