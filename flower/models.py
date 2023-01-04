from django.db import models

# Create your models here.
class Flower(models.Model):
    name = models.CharField(max_length=70)
    species = models.CharField(max_length=70)

class flowerList(models.Model):
    name = models.CharField(max_length=70)
    point =  models.CharField(max_length=70)
    bloom=  models.CharField(max_length=70)
    toxin=  models.CharField(max_length=70)

    def __str__(self):
        return self.name