from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO

from flask_celeryext import FlaskCeleryExt, AppContextTask
from celery import current_app as current_celery_app
from celery import Celery

def make_celery(app):
    celery = current_celery_app
    celery.flask_app = app
    celery.config_from_object(app.config["CELERY_CONFIG"])
    celery.Task = AppContextTask
    return celery

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

ext_celery = FlaskCeleryExt(create_celery_app=make_celery)
#ext_celery = FlaskCeleryExt()
socketio = SocketIO()
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
migrate = Migrate()