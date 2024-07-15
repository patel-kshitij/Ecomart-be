from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, UserUpdateAPIView
from rest_framework_simplejwt.views import TokenRefreshView

''' Basic User management Endpoints'''
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/update/<int:user_id>/', UserUpdateAPIView.as_view(), name='user-update'),
]