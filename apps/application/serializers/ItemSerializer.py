from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.application.models import ItemModel


class ItemSerializer(serializers.ModelSerializer):
    seller_id = serializers.IntegerField(source='seller.id', read_only=True)

    class Meta:
        model = ItemModel
        fields = ('id', 'name', 'description', 'price', 'seller', 'seller_id')
