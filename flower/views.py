
from django.shortcuts import render
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView
from .serializers import flowerSerializer
from .models import flowerList
from .serializers import flowerListSerializer
class ProductListAPI(APIView):
    def get(self, request):
        queryset = flowerList.objects.all()
        print(queryset)
        serializer = flowerListSerializer(queryset, many=True)
        return Response(serializer.data)

class searchID(APIView):
    def get(selt,request,flower_id):
        searchset = flowerList.objects.filter(id=flower_id)
        print(searchset)
        serializer = flowerListSerializer(searchset, many=True)
        return Response(serializer.data)