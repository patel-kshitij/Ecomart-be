from rest_framework import serializers

from apps.application.models import AddressModel


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ('id', 'address_line', 'city', 'state', 'postal_code', 'country')
        read_only_fields = ['id']

    def create(self, validated_data):
        address = AddressModel.objects.create(**validated_data)
        return address

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'address': {
                'id': instance.address.id,
                'address_line': instance.address.address_line,
                'city': instance.address.city,
                'state': instance.address.state,
                'postal_code': instance.address.postal_code,
                'country': instance.address.country
            },
        }

