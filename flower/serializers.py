from rest_framework import serializers
from .models import Flower

# api Serializers

class FlowerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ('name', 's3_url', 'poison')


class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = "__all__"
        
class FlowerHourRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ('name','s3_url' ,'poison','count')

class FlowerTotalRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ('name','s3_url' ,'poison','total_count')
        