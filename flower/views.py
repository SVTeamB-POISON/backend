from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView, exceptions
from .serializers import FlowerSerializer, FlowerNameSerializer
from flower.celery import Celery
from .tasks import descison
import base64



class FlowerDecisionAPI(APIView):

    def post(self, request):
        file = request.FILES['id'].read()
        base64_bs = base64.b64encode(file)
        base64_string = base64_bs.decode('ascii')

        json_list = descison.delay(base64_string)


        return Response(json_list.get(), status=200)

# 꽃 도감 출력, 이름 검색
class FlowerList(APIView):
    def get(self, request):
        queryset = Flower.objects.all()
        serializer = FlowerNameSerializer(queryset, many=True)

        if request.query_params:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.get(name=flower_name)
            serializer = FlowerSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
