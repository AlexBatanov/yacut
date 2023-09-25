from http import HTTPStatus

from flask import jsonify, redirect, request, url_for

from .helpers import chek_and_get_custom_id, chek_and_get_unique, save_url_to_database, validator_api
from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    """Получает длинный URL по короткому идентификатору."""
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(
            'Указанный id не найден', status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url.original})


@app.route('/api/id/', methods=['POST'])
def add_url():
    """Добавляет новый URL в базу данных и возвращает короткую ссылку."""
    data = request.get_json()
    validator_api(data)
    custom_id = chek_and_get_custom_id(data.get('custom_id'))
    save_url_to_database(data['url'], custom_id)
    return jsonify(
        {
            'short_link': url_for(
                'redirect_url', short_link=custom_id, _external=True
            ),
            'url': data['url']
        }
    ), HTTPStatus.CREATED


@app.route('/<string:short_link>')
def redirect_url(short_link):
    """
    Перенаправляет пользователя на оригинальный URL по короткой ссылке.
    """
    return redirect(chek_and_get_unique(short_link).original)
