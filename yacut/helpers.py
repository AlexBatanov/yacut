import random
import re

from .error_handlers import InvalidAPIUsage

from .models import URLMap
from . import db
from .constants import (CHARACTERS, DATA_NOT, MAX_LEN_LINK,
                        NOT_CORRECT_NAME_LINK, NUM_URL_PARTS,
                        REQUERED_URL_FIELD, name_is_ocuppet)


def create_custom_link(castom_id) -> str:
    """Генерирует сокращение для ссылки если кстомная ссылка пустая"""
    if castom_id:
        return castom_id
    custom_id = ''.join(random.sample(CHARACTERS, MAX_LEN_LINK))
    while chek_and_get_unique(custom_id):
        custom_id = create_custom_link()
    return custom_id


def create_short_link(link: str, custom_link: str) -> str:
    """
    Cоздает сокращенную ссылку на основе оригинальной ссылки
    и пользовательского сокращения
    """
    cut_link = '/'.join(link.split('/')[:NUM_URL_PARTS])
    return f'{cut_link}/{custom_link}'


def save_url_to_database(original: str, short: str) -> None:
    """Создает и сохраняет объект в бд"""
    url = URLMap(
        original=original,
        short=short
    )
    db.session.add(url)
    db.session.commit()


def is_english_alphanumeric(input_string: str):
    """
    Проверяет, состоит ли входная строка только из латинских букв и цифр.
    """
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, input_string))


def validator_api(data: dict):
    """
    Проверяет данные запроса API на валидность.
    """
    if not data:
        raise InvalidAPIUsage(DATA_NOT)
    if 'url' not in data:
        raise InvalidAPIUsage(REQUERED_URL_FIELD)


def chek_and_get_custom_id(custom_id) -> str:
    """
    Проверяет кстомную ссылку на валидность и возывращает ее
    """
    custom_id = create_custom_link(custom_id)
    if chek_and_get_unique(custom_id):
        raise InvalidAPIUsage(name_is_ocuppet(custom_id, api=True))
    if len(custom_id) > 16 or not is_english_alphanumeric(custom_id):
        raise InvalidAPIUsage(NOT_CORRECT_NAME_LINK)
    return custom_id


def chek_and_get_unique(custom_id):
    """Проверяет наличие кстомной ссылки в бд и возвращает при ее наличии"""
    return URLMap.query.filter_by(short=custom_id).first()
