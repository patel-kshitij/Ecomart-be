from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.application.models import WishlistModel
from apps.application.serializers import ItemDetailsSerializer


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistModel
        fields = ('id', 'user', 'item')
        read_only_fields = ('id',)

    def create(self, validated_data):
        item = WishlistModel.objects.create(**validated_data)
        return item

    def to_representation(self, list_item):
        return {
            'id': list_item.id,
            'user': UserSerializer(list_item.user).data,
            'item': ItemDetailsSerializer(list_item.item).data,
        }