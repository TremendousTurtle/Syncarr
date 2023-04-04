from flask import (Blueprint, current_app, render_template, request)
import os

from flaskarr.extensions import db, socketio
#from flaskarr.models import Card
#from flaskarr.tasks import process_bulk_data

from celery.result import AsyncResult
from celery import chain


bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')

@bp.route('/test_socketio', methods=['GET'])
def test_socketio():
    socketio.emit('test event', 'whats up yo')
    return {'message': 'emitted test event'}, 202
    