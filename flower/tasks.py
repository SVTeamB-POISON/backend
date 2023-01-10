from __future__ import absolute_import, unicode_literals
from .models import Flower
import requests
from .celery import app
import unicodedata
# Celery task
@app.task
def descison(base64_string):
    
    ai_url = 'http://ai:5001/model'
    
    response = requests.post(ai_url,json={"id":base64_string})
    response = response.json()

    # 상위 3개 꽃 정보 저장
    json_list = []

    for i in response:
        acc, name = i.values()
        # 한글이 자음 모음 형태로 분리되어 깨질 때 해결방안
        name = unicodedata.normalize('NFC',name)
        flower = Flower.objects.get(name=name)

        json_list.append({
            "name": name,
            "s3_url": flower.s3_url,
            "poison": flower.poison,
            "symptom": flower.symptom,
            "scientific_name": flower.scientific_name,
            "flower_language": flower.flower_language,
            "acc": acc
        })

    return json_list
