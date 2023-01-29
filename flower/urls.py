from django.urls import path
from .views import FlowerDecisionAPI, FlowerList, FlowerDetail, FlowerTotalRanking,FlowerHourRanking


urlpatterns = [
    path('', FlowerList.as_view()),
    path('image/', FlowerDecisionAPI.as_view()),
    path('details/', FlowerDetail.as_view()),
    path('total-ranking/', FlowerTotalRanking.as_view()),
    path('hour-ranking/', FlowerHourRanking.as_view()),
]
