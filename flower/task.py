from __future__ import absolute_import
from celery import Celery
from .models import Flower
import requests
import redis

app = Celery('tasks', backend='redis://localhost', broker='pyamqp://guest@localhost//')
rd = redis.StrictRedis(host='localhost', port=6379, db=0)

# app.conf.update(
#         CELERY_TASK_SERIALIZER = 'json',
#         CELERY_RESULT_SERIALIZER = 'json',
#         CELERY_ACCEPT_CONTENT=['json'],
#         CELERY_TIMEZONE = 'Asia/Seoul',
#         CELERY_ENABLE_UTC = True
#                 )

@app.task
def descison(s3_url):
    ai_url = 'http://127.0.0.1:5001/model'
    response = requests.post(ai_url,json={"id": s3_url})
    response = response.json()
    
    json_list = []

    for i in response:

        acc,nam = i.values()
        flower = Flower.objects.get(name=nam)

        json_list.append({
            "name":nam,
            "s3_url":flower.s3_url,
            "poison":flower.poison,
            "symptom":flower.symptom,
            "scientific_name":flower.scientific_name,
            "flower_language":flower.flower_language,
            "acc":acc
        })
    
    return json_list