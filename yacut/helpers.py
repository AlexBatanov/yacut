from .models import URLMap


def get_custom_id(custom_id):
    """Возвращает кастомную ссылку"""
    return URLMap.query.filter_by(short=custom_id).first()