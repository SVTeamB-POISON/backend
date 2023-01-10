from __future__ import absolute_import, unicode_literals
from .models import Flower
import requests
from .celery import app

# Celery task
@app.task
def descison(base64_string):
    
    ai_url = 'http://ai:5001/model'
    
    response = requests.post(ai_url,json={"id":base64_string})
    response = response.json()

    # 상위 3개 꽃 정보 저장
    json_list = []

    for i in response:
        acc, nam = i.values()
        flower = Flower.objects.get(name=nam)

        json_list.append({
            "name": nam,
            "s3_url": flower.s3_url,
            "poison": flower.poison,
            "symptom": flower.symptom,
            "scientific_name": flower.scientific_name,
            "flower_language": flower.flower_language,
            "acc": acc
        })

    return json_list
