from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.accounts.serializers import UserSerializer
from apps.application.models import ItemModel


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ('id', 'name', 'description', 'price', 'seller')
        read_only_fields = ('id',)

    def create(self, validated_data):
        item = ItemModel(**validated_data)
        item.save()
        return item

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class ItemDetailsSerializer(serializers.BaseSerializer):
    def to_representation(self, item):
        return {'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'seller': {'name': item.seller.username,
                           'id': item.seller.id,
                           'first_name': item.seller.first_name,
                           'last_name': item.seller.last_name,
                           'email': item.seller.email
                           }
                }
