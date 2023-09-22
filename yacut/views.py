from flask import flash, redirect, render_template, request, url_for

from . import app
from .forms import URLMapForm
from .models import URLMap
from .helper import create_custom_link, save_url_to_database


@app.route('/', methods=['GET', 'POST'])
def get_add_link():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if not custom_id:
            custom_id = create_custom_link()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('yacut.html', form=form)

        save_url_to_database(form.original_link.data, custom_id)
        return render_template(
            'yacut.html',
            form=form,
            link=form.original_link.data,
            short_link=custom_id, code=302
        )
    return render_template('yacut.html', form=form)

@app.route('/<string:short_link>')
def redirect_view(short_link):
    url = URLMap.query.filter_by(short=short_link).first_or_404()
    return redirect(url.original, code=302)
