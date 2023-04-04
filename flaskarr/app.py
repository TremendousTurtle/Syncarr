import os
from flask import Flask
from flaskarr.extensions import ext_celery, db, ma, migrate, socketio

def create_app(test_config=None, celery_worker=False):
    # create and config app
    flask_app = Flask(__name__, instance_path='/var/lib/syncarr/flaskarr', instance_relative_config=True)
    flask_app.config.from_mapping(
        SECRET_KEY='dev',
        CELERY_CONFIG={
            'broker_url': 'redis://localhost:6379/2',
            'result_backend': 'redis://localhost:6379/2',
            'imports': ['flaskarr.tasks',],
        },
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        DEBUG=True,
        NAV_PAGES={
            'index': 'Home',
            'settings': 'Settings',
        },
        SOCKET_QUEUE='redis://localhost:6379/3',
    )
    
    # ensure the instance folder already exists
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    
    if test_config is None:
        # load instance config, if it exists, when not testing
        flask_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if provided
        flask_app.config.from_mapping(test_config)

    if celery_worker == False:
        socketio.init_app(flask_app, logger=True, engineio_logger=True, message_queue=flask_app.config['SOCKET_QUEUE'])

        
        from flaskarr.events import connect, test_task_event, test_event
    
    db.init_app(flask_app)
    ma.init_app(flask_app)
    migrate.init_app(flask_app, db, render_as_batch=True)
    ext_celery.init_app(flask_app)

    from flaskarr.models import Release, File

    @flask_app.cli.command('createdb')
    def createdb():
        db.create_all()

    from flaskarr.home import bp
    flask_app.register_blueprint(bp)
    flask_app.add_url_rule('/', endpoint='index')
    
    @flask_app.shell_context_processor
    def ctx():
        return {"app": flask_app, "db": db}

    return flask_app