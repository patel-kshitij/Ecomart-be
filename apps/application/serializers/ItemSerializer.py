from rest_framework import serializers

from apps.application.models import ItemModel, ItemImagesModel


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ('id', 'name', 'description', 'price', 'category', 'seller', 'condition')
        read_only_fields = ('id',)

    def create(self, validated_data):
        item = ItemModel.objects.create(**validated_data)
        return item

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.save()
        return instance


class ItemDetailsSerializer(serializers.BaseSerializer):
    def to_representation(self, item):
        item_images = ItemImagesModel.objects.filter(item=item)
        return {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'category': {
                'id': item.category.id,
                'name': item.category.name,
            },
            'seller': {'name': item.seller.username,
                       'id': item.seller.id,
                       'first_name': item.seller.first_name,
                       'last_name': item.seller.last_name,
                       'email': item.seller.email
                       },
            'condition': item.condition,
            'is_sold': item.is_sold,
            'is_bidding_enabled': item.is_bidding_enabled,
            'images': [item_image.image for item_image in item_images],
            'createdAt': item.createdAt,
        }
