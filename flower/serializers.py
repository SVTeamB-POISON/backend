
from rest_framework import serializers
from .models import Flower
from .models import flowerList

class flowerSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Flower        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함

class flowerListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = flowerList        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함