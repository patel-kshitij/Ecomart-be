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

    def update(self, instance, validated_data):
        instance.apartment = validated_data.get('apartment', instance.apartment)
        instance.address_line = validated_data.get('address_line', instance.address_line)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.country = validated_data.get('country', instance.country)
        instance.save()

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

