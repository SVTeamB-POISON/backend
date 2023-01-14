from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView, exceptions
from .serializers import FlowerSerializer, FlowerNameSerializer, FlowerHourRankingSerializer,FlowerTotalRankingSerializer
from .tasks import descison
import base64
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# 이미지 업로드, AI 판단 후 탑3 꽃 응답
class FlowerDecisionAPI(APIView):
    type = openapi.Parameter('id', openapi.IN_FORM, description='Document to be uploaded',type=openapi.TYPE_FILE)
    
    @swagger_auto_schema(operation_id='Create a document',operation_description='Create a document by providing file',manual_parameters=[type])
    def post(self, request):
        file = request.FILES['id'].read()
        base64_bs = base64.b64encode(file)
        base64_string = base64_bs.decode('ascii')

        # Celery 비동기 처리
        json_list = descison.delay(base64_string)

        return Response(json_list.get(), status=200)


# 꽃 도감 출력(pagination), 이름 검색,
class FlowerList(APIView):
    name = openapi.Parameter('name', openapi.IN_QUERY, description='search parm', required=False, type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], manual_parameters=[name], responses={200: 'Success'})
    def get(self, request):
        pre_page_num = None
        next_page_num = None
        naming = None
        
        page = request.GET.get('page', '1')
        name = request.GET.get('name', None)

        # 이름 순으로 정렬후 paginationhttps://coding-kindergarten.tistory.com/164
        flower_list = Flower.objects.all().order_by('name')

        # 파라미터가 name 이면 해당 꽃 정보 제공
        if name :
            flower_name = request.query_params.get('name', None)
            flower_list = Flower.objects.filter(name__contains=flower_name).order_by('name')
        
        paginator = Paginator(flower_list, 6)
        flower_obj = paginator.get_page(page)

        queryset = paginator.page(flower_obj.number)
        serializer = FlowerNameSerializer(queryset,many=True)

        pre = flower_obj.has_previous()
        next = flower_obj.has_next()
        
        if name is None:
            name=""
        try:
            prevPage="/flowers?page="+str(flower_obj.previous_page_number())+"&name="+name
        except:
            prevPage=None        
        try:
            nextPage="/flowers?page="+str(flower_obj.next_page_number())+"&name="+name
        except:
            nextPage=None

        data = {"hasNextPage": next, "hasPrevPage": pre,
                "nextPage": nextPage,
                "prevPage": prevPage,
                "data": serializer.data}
        
        return Response(data)


# 꽃 세부 정보
class FlowerDetail(APIView):
    name = openapi.Parameter('name', openapi.IN_QUERY, description='name parm', required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(tags=['지정한 데이터의 상세 정보를 불러옵니다.'], manual_parameters=[name], responses={200: 'Success'})
    def get(self, request):
        if request.query_params:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.get(name=flower_name)
            serializer = FlowerSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FlowerHourRanking(APIView):

    def get(self, request):
        ranking_list = Flower.objects.all().order_by('-count')
        serializer = FlowerHourRankingSerializer(ranking_list[:6], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FlowerTotalRanking(APIView):
    def get(self, request):
        ranking_list = Flower.objects.all().order_by('-total_count')
        serializer = FlowerTotalRankingSerializer(ranking_list[:6], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)