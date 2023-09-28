import random

from .validators import validator_custom_id_api, validator_custom_id_views
from .models import URLMap
from . import db
from .constants import CHARACTERS, MAX_LEN_LINK
from .helpers import get_custom_id


def generate_custom_id() -> str:
    """Генерирует сокращение для ссылки"""
    custom_id = ''.join(random.sample(CHARACTERS, MAX_LEN_LINK))
    while get_custom_id(custom_id):
        custom_id = generate_custom_id()
    return custom_id


def save_url_to_database(original: str, short: str) -> None:
    """Создает и сохраняет объект в бд"""
    url = URLMap(
        original=original,
        short=short
    )
    db.session.add(url)
    db.session.commit()


def chek_and_get_custom_id(data, is_api=True) -> str:
    """
    Проверяет кастомную ссылку на валидность при отсутсвие генерируется,
    и сохраняет в бд
    """
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = generate_custom_id()
    if is_api:
        validator_custom_id_api(custom_id)
    else:
        validator_custom_id_views(custom_id)
    save_url_to_database(data.get('url'), custom_id)
    return custom_id
