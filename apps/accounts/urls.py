from django.urls import path
from .views import (RegisterView, CustomTokenObtainPairView, UserUpdateAPIView, PasswordResetAPIView,
                    PasswordResetConfirmAPIView)
from rest_framework_simplejwt.views import TokenRefreshView

''' Basic User management Endpoints'''
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/update/<int:user_id>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('reset-password/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('reset-password-confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]
