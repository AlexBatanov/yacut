from http import HTTPStatus

from flask import flash, redirect, render_template

from .error_handlers import InvalidAPIUsage
from . import app
from .forms import URLMapForm
from .models import URLMap
from .services import chek_and_get_custom_id
from .constants import name_is_ocuppet


@app.route('/', methods=['GET', 'POST'])
def get_add_link():
    """
    Обрабатывает GET и POST запросы для отображения формы
    и добавления новой ссылки.
    """
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    custom_id = form.custom_id.data
    try:
        custom_id = chek_and_get_custom_id(form.to_dict())
    except InvalidAPIUsage:
        flash(name_is_ocuppet(custom_id))
        return render_template('yacut.html', form=form)

    return render_template(
        'yacut.html',
        form=form,
        link=form.original_link.data,
        short_link=custom_id,
        code=HTTPStatus.FOUND
    )


@app.route('/<string:short_link>')
def redirect_view(short_link):
    """
    Перенаправляет пользователя на оригинальный URL по короткой ссылке.
    """
    url = URLMap.query.filter_by(short=short_link).first_or_404()
    return redirect(url.original)
