from rest_framework import serializers

from apps.application.models import AddressModel


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ('id', 'apartment', 'address_line', 'city', 'state', 'postal_code', 'country')
        read_only_fields = ['id']

    def create(self, validated_data):
        address = AddressModel.objects.create(**validated_data)
        return address

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'apartment': instance.apartment,
            'address_line': instance.address_line,
            'city': instance.city,
            'state': instance.state,
            'postal_code': instance.postal_code,
            'country': instance.country
        }

