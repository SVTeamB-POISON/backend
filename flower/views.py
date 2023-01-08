
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView
from .serializers import FlowerSerializer
from celery import Celery
import requests
from django.http import HttpResponse, JsonResponse
import json
from .task import descison



class FlowerDecisionAPI(APIView):
    
    def post(self,request):

    
        # image to S3 , S3_url to backend
        
        s3_url = "https://img.freepik.com/free-photo/purple-osteospermum-daisy-flower_1373-16.jpg?w=2000"
        
        json_list = descison.delay(s3_url)

        # ai 서버에서 반환 이후.
        while True:
            if json_list.ready():
                print(json_list.result)
                break
        
        return Response({'id':str(json_list.result)},status=200)

