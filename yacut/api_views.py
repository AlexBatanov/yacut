from flask import jsonify, redirect, request, url_for

from .helper import create_custom_link, create_short_link, is_english_alphanumeric
from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return jsonify({'url':url.original}), 200

@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    custom_id = data.get('custom_id')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not custom_id:
        custom_id = create_custom_link()
    elif URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.', status_code=400)
    if len(custom_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', status_code=400)
    if not is_english_alphanumeric(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', status_code=400)
    data['custom_id'] = custom_id
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify({'short_link': url_for('redirect_url', short_link=data['custom_id'], _external=True), 'url': data['url']}), 201

@app.route('/<string:short_link>')
def redirect_url(short_link):
    url = URLMap.query.filter_by(short=short_link).first()
    if not url:
        return jsonify({'error': 'Короткая ссылка не найдена'}), 404
    return redirect(url.original, code=302)