from flask import (Blueprint, current_app, render_template, request)
import os

from flaskarr.extensions import db, socketio
from flaskarr.models import File, Release
from flaskarr.tasks import example_task, emit_test_task_event

from celery.result import AsyncResult
from celery import chain


bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

@bp.route('/test_socketio', methods=['GET'])
def test_socketio():
    socketio.emit('test event', 'whats up yo')
    return {'message': 'emitted test event'}, 202
    