from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    id = serializers.CharField()
    new_password = serializers.CharField()
