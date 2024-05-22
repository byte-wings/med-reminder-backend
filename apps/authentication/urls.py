from django.urls import path
from .views import (
    UserAuthView,
    VerifyCodeView,
    CustomTokenRefreshView,
    LogoutView
)

urlpatterns = [
    path('', UserAuthView.as_view(), name='authentication'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
