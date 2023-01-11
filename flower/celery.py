from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('flower',
             broker='pyamqp://guest@localhost//',
             backend='redis://localhost',
             include=['flower.tasks'])
app.autodiscover_tasks()
# 도커 테스트
# Celery 설정
# app = Celery('flower',
#              broker='pyamqp://guest@rb:5672//',
#              backend='redis://rd',
#              include=['flower.tasks'])

#(선택) 추가설정
app.conf.update(
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True,
    CELERYBEAT_SCHEDULE = {
        'update_rangking': {
            'task': 'tasks.ranking_schedule',
            'schedule': timedelta(seconds=1),
            'args': ()
        }
    }      
)

if __name__ == '__main__':
    app.start()