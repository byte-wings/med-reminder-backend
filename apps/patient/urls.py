from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, DrugViewSet


router = DefaultRouter()
router.register(r'', PatientViewSet)
router.register(r'drugs', DrugViewSet, basename='drug')

urlpatterns = [
    path('', include(router.urls)),
]
