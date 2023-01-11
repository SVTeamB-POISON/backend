from djongo import models


# Flower 컬렉션
class Flower(models.Model):
    name = models.CharField(max_length=70)
    s3_url = models.TextField()
    poison = models.BooleanField(default=False)
    symptom = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    flower_language = models.CharField(max_length=100)
    detail = models.TextField()
    count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)