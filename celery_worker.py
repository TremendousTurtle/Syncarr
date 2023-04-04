from flaskarr.app import create_app
from flaskarr.extensions import ext_celery

app = create_app(celery_worker=True)
celery = ext_celery.celery