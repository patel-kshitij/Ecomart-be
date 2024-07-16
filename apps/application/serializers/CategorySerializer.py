from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.application.models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        category = CategoryModel(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    def to_representation(self, item):
        return {
            'id': item.id,
            'name': item.name
        }
