#!/bin/zsh
# Start celery worker
cd /code/Syncarr
#celery -A celery_worker.celery worker --loglevel=info
source /code/Syncarr/venv/bin/activate
celery -A celery_worker.celery multi start w1 --pidfile=/run/celery/%%n.pid --logfile=/var/log/celery/%%n%%I.log --loglevel="INFO"