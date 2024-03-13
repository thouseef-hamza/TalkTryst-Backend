from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.UserRegistrationAPIView.as_view(),name="registration"),
    path("otp/verify",views.OTPVerificationAPIView.as_view(),name="otp_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
