
from django.shortcuts import render
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView
from .serializers import flowerSerializer
from .models import flowerList
from .serializers import flowerListSerializer
from celery import Celery
import requests
from django.http import HttpResponse
import json

app = Celery('tasks', broker='pyamqp://guest@localhost//')
class ProductListAPI(APIView):
    def get(self, request):
        queryset = flowerList.objects.all()
        print(queryset)
        serializer = flowerListSerializer(queryset, many=True)
        return Response(serializer.data)
    
#    @app.task
    def post(self,request):
        image_url = request.POST.get('id')
        print(image_url)
        json1 = {"id":image_url}
        url = 'http://localhost:5001/model'
        json2 = requests.post(url,json1)
        
        return HttpResponse(json.dumps(json2), content_type = "application/json")
    # def post(self,request):
    #     image_url = request.POST.get('id')
    #     image_url.save()
    #     json={"id":image_url}
    #     url = 'http://localhost:5001/model'
    #     json2 = requests.post(url,json)
    #     return Response(json2, status=status.HTTP_201_CREATED)
    
class searchID(APIView):
    def get(self,request,flower_id):
        searchset = flowerList.objects.filter(id=flower_id)
        print(searchset)
        serializer = flowerListSerializer(searchset, many=True)
        return Response(serializer.data)
