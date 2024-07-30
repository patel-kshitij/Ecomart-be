from rest_framework import serializers

from apps.application.models import (OrderModel, ItemModel, OrderContactDetailsModel, OrderItemModel,
                                     ShippingAddressModel)
from apps.application.serializers import ItemDetailsSerializer
from apps.application.serializers import AddressSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddressModel
        fields = ('id', 'user', 'address')
        read_only_fields = ['id']

    def create(self, validated_data):
        shipping_address = ShippingAddressModel.objects.create(**validated_data)
        return shipping_address

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'address': AddressSerializer(instance.address).data,
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ('id', 'user', 'shipping_address', 'billing_address', 'contact_details')
        read_only_fields = ('id',)

    def create(self, validated_data):
        order = OrderModel.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.billing_address = validated_data.get('billing_address', instance.billing_address)
        instance.contact_details = validated_data.get('contact_details', instance.contact_details)

        instance.save()
        return instance


class OrderDetailsSerializer(serializers.BaseSerializer):
    def to_representation(self, order: OrderModel):
        order_items = OrderItemModel.objects.filter(order_id=order.id)

        return {
            'id': order.id,
            'user': {
                'name': order.user.username,
                'id': order.user.id,
                'first_name': order.user.first_name,
                'last_name': order.user.last_name,
                'email': order.user.email
            },
            'shipping_address': (ShippingAddressSerializer(order.shipping_address).data.get('address')),
            'billing_address': AddressSerializer(order.billing_address).data.get('address'),
            'items': [ItemDetailsSerializer(order_item.item) for order_item in order_items],
            'contact_details': {
                'id': order.contact_details.id,
                'first_name': order.contact_details.first_name,
                'last_name': order.contact_details.last_name,
                'email': order.contact_details.email,
                'phone': order.contact_details.phone,
            },
            'createdAt': order.createdAt,
        }
