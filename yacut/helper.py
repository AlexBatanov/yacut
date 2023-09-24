import random
import re

from .error_handlers import InvalidAPIUsage

from .models import URLMap
from . import db
from .constants import (CHARACTERS, DATA_NOT, MAX_LEN_LINK,
                        NOT_CORRECT_NAME_LINK, NUM_URL_PARTS,
                        REQUERED_URL_FIELD, name_is_ocuppet)


def create_custom_link() -> str:
    """Генерирует сокращение для ссылки"""
    custom_link = ''.join(random.sample(CHARACTERS, MAX_LEN_LINK))
    while URLMap.query.filter_by(short=custom_link).first():
        custom_link = create_custom_link()
    return custom_link


def create_short_link(link: str, custom_link: str) -> str:
    """
    Cоздает сокращенную ссылку на основе оригинальной ссылки
    и пользовательского сокращения
    """
    cut_link = '/'.join(link.split("/")[:NUM_URL_PARTS])
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
    Проверяет данные запроса API на валидность и вносит необходимые изменения.
    """
    if not data:
        raise InvalidAPIUsage(DATA_NOT)
    custom_id = data.get('custom_id')
    if 'url' not in data:
        raise InvalidAPIUsage(REQUERED_URL_FIELD)
    if not custom_id:
        custom_id = create_custom_link()
    elif URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(name_is_ocuppet(custom_id, api=True))
    if len(custom_id) > 16 or not is_english_alphanumeric(custom_id):
        raise InvalidAPIUsage(NOT_CORRECT_NAME_LINK)
    data['custom_id'] = custom_id
