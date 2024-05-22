from django.urls import path
from .views import PredictDisease

urlpatterns = [
    path('', PredictDisease.as_view(), name='predict-disease'),
]
