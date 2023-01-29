from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('flower',
#              broker='pyamqp://guest@localhost//',
#              backend='redis://localhost',
#              include=['flower.tasks'])
# 도커 테스트
# Celery 설정
app = Celery('flower',
             broker='pyamqp://guest@172.17.0.1:5672//', # docker-network bridge localhost 
             backend='redis://172.17.0.1:6379', 
             include=['flower.tasks'])

app.conf.worker_max_tasks_per_child = 100

#(선택) 추가설정

if __name__ == '__main__':
    app.start()

