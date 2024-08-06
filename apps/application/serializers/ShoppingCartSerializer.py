from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.application.models import ShoppingCartModel
from apps.application.serializers import ItemSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartModel
        fields = ('id', 'user', 'item', 'quantity')
        read_only_fields = ('id',)

    def create(self, validated_data):
        item = ShoppingCartModel.objects.create(**validated_data)
        return item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def to_representation(self, cart_item):
        return {
            'id': cart_item.id,
            'user': UserSerializer(cart_item.user).data,
            'item': ItemSerializer(cart_item.item).data,
            'quantity': cart_item.quantity,
        }