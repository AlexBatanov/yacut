import random

from .constants import CHARACTERS, MAX_LEN_LINK, NUM_URL_PARTS
from .models import URLMap
from . import db


def create_custom_link() -> str:
    """Генерирует сокращение для ссылки"""
    custom_link = ''.join(random.sample(CHARACTERS, MAX_LEN_LINK))
    while URLMap.query.filter_by(short=custom_link).first():
        custom_link = create_custom_link()
    return custom_link


def create_short_link(link:str, custom_link:str) -> str:
    """
    Cоздает сокращенную ссылку на основе оригинальной ссылки
    и пользовательского сокращения
    """
    cut_link = '/'.join(link.split("/")[:NUM_URL_PARTS])
    return f'{cut_link}/{custom_link}'


def save_url_to_database(original:str, short:str) -> None:
    """Создает и сохраняет объект в бд"""
    url = URLMap(
        original=original,
        short=short
    )
    db.session.add(url)
    db.session.commit()
