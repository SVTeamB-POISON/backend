from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('flower',
#              broker='pyamqp://guest@localhost//',
#              backend='redis://localhost',
#              include=['flower.tasks'])
# 도커 테스트
app = Celery('flower',
             broker='pyamqp://guest@rb:5672//',
             backend='redis://rd',
             include=['flower.tasks'])

#(선택) 추가설정
app.conf.update(
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
)

if __name__ == '__main__':
    app.start()