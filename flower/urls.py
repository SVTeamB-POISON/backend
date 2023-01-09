from django.urls import path
from .views import FlowerDecisionAPI, FlowerList

urlpatterns = [
    path('', FlowerList.as_view()),
    path('upload/', FlowerDecisionAPI.as_view()),
]
