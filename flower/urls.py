from django.urls import path
from .views import FlowerDecisionAPI, FlowerList, FlowerDetail, FlowerRanking


urlpatterns = [
    path('', FlowerList.as_view()),
    path('image/', FlowerDecisionAPI.as_view()),
    path('details/', FlowerDetail.as_view()),
    path('ranking/', FlowerRanking.as_view())
]
