from flaskarr.extensions import db, ma
from celery import group, chain, chord, shared_task
from flask_celeryext import AppContextTask
from datetime import datetime
from flaskarr.models import Release, File
import requests
import os
import hashlib
import shutil
from flask_socketio import SocketIO
from flask import current_app
import threading
from collections.abc import Callable

class SocketTask(AppContextTask):
    _sio = None
    _lock = None
    
    @property
    def sio(self):
        if self._sio is None:
            self._sio = SocketIO(message_queue=current_app.config['SOCKET_QUEUE'])
        return self._sio
    
    @property
    def lock(self):
        if self._lock is None:
            self._lock = threading.Lock()
        return self._lock
    
    def emit(self, event: str, data=None, namespace: str = None, callback: Callable =  None):
        with self.lock:
            self.sio.emit(event, data=data, namespace=namespace, callback=callback)
            
    def emit_error(self, error: str, details: dict, where: str = None, sender: str = 'task', event: str = '_error'):
        data = {}
        if where is not None:
            data['where'] = where
        else:
            data['where'] = 'none'
            
        data.update({
            'details': details,
            'error': error,
            'sender': sender.strip().lower(),
        })
            
        self.emit(event, data=data)

@shared_task(base=SocketTask, bind=True)
def example_task(self):
    self.emit('starter chained task', self.request.id)

@shared_task(base=SocketTask, bind=True)
def emit_test_task_event(self):
    self.emit('task triggered event')