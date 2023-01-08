from django.urls import path
from . import views
from .views import FlowerDecisionAPI

urlpatterns = [
	path('upload/', FlowerDecisionAPI.as_view()),
    #path('<int:flower_id>/', searchID.as_view()),
]