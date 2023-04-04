import eventlet
eventlet.monkey_patch(socket=True)
from flaskarr.app import create_app
from flaskarr.extensions import ext_celery, socketio

app = create_app()
celery = ext_celery.celery

if __name__ == '__main__':
    socketio.run(app, debug=False, log_output=True, host='0.0.0.0', port='5050', use_reloader=True)