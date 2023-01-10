from django.urls import path
from .views import FlowerDecisionAPI, FlowerList, FlowerDetail


urlpatterns = [
    path('', FlowerList.as_view()),
    path('upload/', FlowerDecisionAPI.as_view()),
    path('details/', FlowerDetail.as_view())
]
