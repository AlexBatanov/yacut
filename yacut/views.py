from flask import flash, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap
from .helper import (create_custom_link, create_short_link,
                     save_url_to_database)


# @app.route('/', methods=['GET'])
# def index_view():
#     form = URLMapForm()
#     return render_template('yacut.html', form=form), 200


@app.route('/', methods=['GET', 'POST'])
def add_link():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if not custom_id:
            custom_id = create_custom_link()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('yacut.html', form=form)

        save_url_to_database(form.original_link.data, custom_id)
        short_link = create_short_link(form.original_link.data, custom_id)
        return render_template(
            'yacut.html',
            form=form,
            link=form.original_link.data,
            short_link=short_link, code=302
        )

    return render_template('yacut.html', form=form)

