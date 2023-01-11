from rest_framework import status
from rest_framework.response import Response
from .models import Flower
from rest_framework.views import APIView, exceptions
from .serializers import FlowerSerializer, FlowerNameSerializer
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


# 꽃 도감 출력(pagination), 이름 검색,
class FlowerList(APIView):

    def get(self, request):
        page = request.GET.get('page', '1')
        flower_list = Flower.objects.order_by('id')
        paginator = Paginator(flower_list, 6)
        flower_obj = paginator.get_page(page)
        queryset = Flower.objects.filter(id__lte=6)
        serializer = FlowerNameSerializer(queryset, many=True)

        name = request.GET.get('name', None)
        page = request.GET.get('page', None)

        if name:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.filter(name__contains=flower_name)
            serializer = FlowerNameSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif page:
            if flower_obj.number == 1:
                queryset = Flower.objects.filter(id__lte=6)
            else:
                queryset = Flower.objects.filter(id__gt=6 * (flower_obj.number - 1)).filter(
                    id__lte=(6 * flower_obj.number))

            serializer = FlowerNameSerializer(queryset, many=True)

        if flower_obj.has_previous():
            if flower_obj.has_next():
                return Response({"hasNextPage": True, "hasPrevPage": True,
                                 "nextPage": "api/flowers?page=" + str(flower_obj.next_page_number()),
                                 "prevPage": "api/flowers?page=" + str(flower_obj.previous_page_number()),
                                 "data": serializer.data})
            else:
                return Response({"hasNextPage": False, "hasPrevPage": True,
                                 "nextPage": None,
                                 "prevPage": "api/flowers?page=" + str(flower_obj.previous_page_number()),
                                 "data": serializer.data})

        else:
            return Response({"hasNextPage": True, "hasPrevPage": False,
                             "nextPage": "api/flowers?page=" + str(flower_obj.next_page_number()),
                             "prevPage": None, "data": serializer.data})


# 꽃 세부 정보
class FlowerDetail(APIView):
    def get(self, request):
        if request.query_params:
            flower_name = request.query_params.get('name', None)
            queryset = Flower.objects.get(name=flower_name)
            serializer = FlowerSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)
