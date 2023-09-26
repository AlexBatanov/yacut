import logging
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Настройка обработчика логов для вывода в консоль
handler = logging.StreamHandler()
app.logger.addHandler(handler)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import error_handlers, views, api_views, models, services, validators, constants