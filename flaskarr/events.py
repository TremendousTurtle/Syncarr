from flaskarr.extensions import socketio, db
from flaskarr.models import Release, File
from flask_socketio import emit, join_room, rooms, ConnectionRefusedError
from flask import request, current_app
from flaskarr.tasks import example_task, emit_test_task_event
from celery.result import AsyncResult
from celery import chain


###################### Core Event Handlers ######################
# Handlers for core/basic events like connect
    
@socketio.on('connect')
def connect(auth=None):
    if auth is None or auth.get('id', None) is None:
        raise ConnectionRefusedError('missing auth id')
    else:
        current_app.logger.info(f'connected sid: {request.sid} id: {auth["id"]}')
        join_room(auth['id'])
        return True
    
###################### Test Event Handlers ######################
# Handlers for events for testing

@socketio.on('test task event')
def test_task_event():
    emit_test_task_event.si().apply_async()
    
@socketio.on('test event')
def test_event(data):
    print(f'Got test event: {data} from sid: {request.sid}')