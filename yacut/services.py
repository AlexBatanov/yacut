import random

from . import app
from .validators import validator_custom_id
app.logger.info('servivs')
from .models import URLMap
from . import db
from .constants import CHARACTERS, MAX_LEN_LINK

def generate_custom_id() -> str:
    """Генерирует сокращение для ссылки"""
    custom_id = ''.join(random.sample(CHARACTERS, MAX_LEN_LINK))
    while get_custom_id(custom_id):
        custom_id = generate_custom_id()
    return custom_id


# def create_short_link(link: str, custom_link: str) -> str:
#     """
#     Cоздает сокращенную ссылку на основе оригинальной ссылки
#     и пользовательского сокращения
#     """
#     cut_link = '/'.join(link.split('/')[:NUM_URL_PARTS])
#     return f'{cut_link}/{custom_link}'


def save_url_to_database(original: str, short: str) -> None:
    """Создает и сохраняет объект в бд"""
    url = URLMap(
        original=original,
        short=short
    )
    db.session.add(url)
    db.session.commit()


def chek_and_get_custom_id(data) -> str:
    """
    Проверяет кастомную ссылку на валидность при отсутсвие генерируется
    """
    custom_id = data.get('custom_id')
    if not custom_id:
        return generate_custom_id()
    validator_custom_id(custom_id)
    return custom_id


def get_custom_id(custom_id):
    """Возвращает кастомную ссылку"""
    return URLMap.query.filter_by(short=custom_id).first()
