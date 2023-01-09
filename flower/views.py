from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView, exceptions
from .serializers import FlowerSerializer, FlowerNameSerializer
from flower.celery import Celery
import requests
from django.http import HttpResponse, JsonResponse
import json
from .tasks import descison
import time
import redis


from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder


class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
            return o.read()
        return str(o)


class FlowerDecisionAPI(APIView):

    def post(self, request):
        # image to S3 , S3_url to backend
        file = request.FILES['id']
        obj = {
            'id': file
        }

        json_list = descison.delay(json.dumps(obj, cls=MyJsonEncoder))

        return Response(json_list.get(), status=200)


class FlowerList(APIView):
    def get(self, request):
        queryset = Flower.objects.all()
        serializer = FlowerNameSerializer(queryset, many=True)

        if request.query_params:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.get(name=flower_name)
            serializer = FlowerNameSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FlowerDetail(APIView):
    def get(self, request):
        if request.query_params:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.get(name=flower_name)
            serializer = FlowerSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)
