from django.urls import path
from .views import UserDetailView, UserUpdateView

urlpatterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('me/update/', UserUpdateView.as_view(), name='user-update'),
]