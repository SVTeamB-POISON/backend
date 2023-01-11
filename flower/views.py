from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView, exceptions
from .serializers import FlowerSerializer, FlowerNameSerializer
from flower.celery import Celery
from .tasks import descison
import base64
from django.core.paginator import Paginator


# 이미지 업로드, AI 판단 후 탑3 꽃 응답
class FlowerDecisionAPI(APIView):

    def post(self, request):
        file = request.FILES['id'].read()
        base64_bs = base64.b64encode(file)
        base64_string = base64_bs.decode('ascii')

        # Celery 비동기 처리
        json_list = descison.delay(base64_string)

        return Response(json_list.get(), status=200)


# 꽃 도감 출력(무한 스크롤), 이름 검색,
class FlowerList(APIView):

    def get(self, request):
        page = request.GET.get('page', '1')
        name = request.GET.get('name', None)
        
        # 이름 순으로 정렬후 pagination
        flower_list = Flower.objects.order_by('name')
        paginator = Paginator(flower_list, 6)
        flower_obj = paginator.get_page(page)

        # 파라미터가 name 이면 해당 꽃 정보 제공
        if name:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.filter(name__contains=flower_name)
            serializer = FlowerNameSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = paginator.page(flower_obj.number)
        serializer = FlowerNameSerializer(queryset,many=True)
        
        pre = flower_obj.has_previous()
        next = flower_obj.has_next()

        if (pre&next):
            prePage = "api/flowers?page=" + str(flower_obj.previous_page_number())
            nextPage = "api/flowers?page=" + str(flower_obj.next_page_number())
        else:
            if(pre):
                prePage = "api/flowers?page=" + str(flower_obj.previous_page_number())
                nextPage = None
            else:
                prePage = None
                nextPage = "api/flowers?page=" + str(flower_obj.next_page_number())

        data = {"hasNextPage": next, "hasPrevPage": pre,
                "nextPage": nextPage,
                "prevPage": prePage,
                "data": serializer.data}

        return Response(data)

# 꽃 세부 정보
class FlowerDetail(APIView):
    def get(self, request):
        if request.query_params:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.get(name=flower_name)
            serializer = FlowerSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)
