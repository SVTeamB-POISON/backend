from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView
from .serializers import FlowerSerializer, FlowerNameSerializer
from flower.celery import Celery
import requests
from django.http import HttpResponse, JsonResponse
import json
from .tasks import descison
import time
import redis


class FlowerDecisionAPI(APIView):

    def post(self, request):
        # image to S3 , S3_url to backend

        s3_url = "https://img.freepik.com/free-photo/purple-osteospermum-daisy-flower_1373-16.jpg?w=2000"

        json_list = descison.delay(s3_url)

        return Response(json_list.get(), status=200)


# 꽃 도감 출력
class FlowerList(APIView):
    def get(self, request):
        queryset = Flower.objects.all()
        serializer = FlowerNameSerializer(queryset, many=True)
        return Response(serializer.data)


# 꽃 이름으로 검색
class SearchName(APIView):
    def get(self, request, flower_name):
        queryset = Flower.objects.filter(name=flower_name)
        serializer = FlowerSerializer(queryset, many=True)

        return Response(serializer.data)
