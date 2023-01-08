from rest_framework import serializers
from .models import Flower


class FlowerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ('name', 's3_url', 'poison')


class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = "__all__"
