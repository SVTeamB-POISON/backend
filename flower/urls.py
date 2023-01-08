from django.urls import path
from . import views
from .views import FlowerDecisionAPI, SearchName, FlowerList

urlpatterns = [
    path('', FlowerList.as_view()),
    path('upload/', FlowerDecisionAPI.as_view()),
    path('<str:flower_name>/', SearchName.as_view()),
]
