from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response

from apps.accounts.serializers import UserSerializer

User = get_user_model()


class UserDetailsView(generics.CreateAPIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
