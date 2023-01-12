from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from celery.schedules import crontab
from datetime import timedelta
import sys
from kombu.utils import encoding
sys.modules['celery.utils.encoding'] = encoding
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('flower',
             broker='pyamqp://guest@localhost//',
             backend='redis://localhost',
             include=['flower.tasks'])
# 도커 테스트
# Celery 설정
# app = Celery('flower',
#              broker='pyamqp://guest@rb:5672//',
#              backend='redis://rd',
#              include=['flower.tasks'])

#(선택) 추가설정

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler',
    SELERY_BEAT_SCHEDULE = {
    'add-every-30-seconds': {  # 스케쥴링의 이름
        'task': 'tasks.add',   # 수행해줄 task 설정
        'schedule': 30.0,      # 수행할 시간 설정
        'args': (16, 16)       # 인풋값 설정
    },
}
)
django.setup()

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()








app.autodiscover_tasks()
