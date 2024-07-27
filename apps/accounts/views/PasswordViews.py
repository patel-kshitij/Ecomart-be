# views.py
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail, BadHeaderError
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from EcoMart import settings
from ..serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.urls import reverse

User = get_user_model()


class PasswordResetAPIView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.html"
                context = {
                    "email": user.email,
                    'domain': 'localhost:8000',  # TODO: Change this domain and take this to some env file.
                    'site_name': 'EcoMart',
                    "id": urlsafe_base64_encode(force_bytes(user.id)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, context)
                try:
                    send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                except BadHeaderError:
                    return Response({"message": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)
            return Response({"email": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):

    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_id = force_str(urlsafe_base64_decode(serializer.validated_data['id']))
                user = User.objects.get(id=user_id)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, serializer.validated_data['token']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
