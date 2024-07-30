from rest_framework import serializers

from apps.application.models import (OrderModel, ItemModel, ContactDetailsModel, OrderItemModel,
                                     ShippingAddressModel)
from apps.application.serializers import ItemDetailsSerializer
from apps.application.serializers import AddressSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddressModel
        fields = ('id', 'user', 'address')
        read_only_fields = ('id',)

    def create(self, validated_data):
        shipping_address = ShippingAddressModel.objects.create(**validated_data)
        return ShippingAddressSerializer(shipping_address).data

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


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetailsModel
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')
        read_only_fields = ('id',)

    def create(self, validated_data):
        order_contact = ContactDetailsModel.objects.create(**validated_data)
        return order_contact

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'phone': instance.phone,
        }


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
            'shipping_address': ShippingAddressSerializer(order.shipping_address).data.get('address'),
            'billing_address': AddressSerializer(order.billing_address).data,
            'items': [ItemDetailsSerializer(order_item.item).data for order_item in order_items],
            'contact_details': ContactDetailsSerializer(order.contact_details).data,
            'createdAt': order.createdAt,
        }
