from django.core.paginator import Paginator
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import OrderModel, OrderItemModel, ShippingAddressModel
from ..serializers import OrderSerializer, ShippingAddressSerializer, AddressSerializer, \
    ContactDetailsSerializer, OrderDetailsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_shipping_address(request):
    user = request.user
    user_id = user.id

    address_serializer = AddressSerializer(data=request.data)
    address_serializer.is_valid(raise_exception=True)
    address_serializer.save()

    address_id = address_serializer.data.get('id')

    shipping_address_serializer = ShippingAddressSerializer(data={
        'user': user_id,
        'address': address_id,
    })

    shipping_address_serializer.is_valid(raise_exception=True)
    shipping_address = shipping_address_serializer.save()

    return Response(shipping_address, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shipping_addresses(request):
    user = request.user
    user_id = user.id

    shipping_addresses = ShippingAddressModel.objects.filter(user=user_id)
    serializer = ShippingAddressSerializer(shipping_addresses, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_order(request):
    user = request.user
    user_id = user.id

    request_data = request.data

    shipping_address_id = request_data.get('shipping_address')
    try:
        shipping_address = ShippingAddressModel.objects.get(id=shipping_address_id)
    except ShippingAddressModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Shipping address not found'})

    billing_address = request_data.get('billing_address', None)
    if not billing_address:
        billing_address_id = shipping_address.address.id
    else:
        billing_address_serializer = AddressSerializer(data=billing_address)
        billing_address_serializer.is_valid(raise_exception=True)
        billing_address_serializer.save()
        billing_address_id = billing_address_serializer.data.get('id')

    contact_details = request_data.get('contact_details')

    contact_details_serializer = ContactDetailsSerializer(data=contact_details)
    contact_details_serializer.is_valid(raise_exception=True)
    contact_details_serializer.save()

    contact_details_id = contact_details_serializer.data.get('id')

    order_serializer = OrderSerializer(data={
        'user': user_id,
        'shipping_address': shipping_address_id,
        'billing_address': billing_address_id,
        'contact_details': contact_details_id,
    })

    order_serializer.is_valid(raise_exception=True)
    order_serializer.save()

    order_id = order_serializer.data.get('id')

    items = request_data.get('items')

    for item in items:
        OrderItemModel.objects.create(order_id=order_id, item_id=item)

    order = OrderModel.objects.get(id=order_id)

    return Response(OrderDetailsSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    user_id = user.id
    orders = OrderModel.objects.filter(user_id=user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_details(request, order_id):
    order = OrderModel.objects.get(id=order_id)
    serializer = OrderDetailsSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_details(request, order_id):
    user = request.user
    user_id = user.id
    order = OrderModel.objects.get(id=order_id)

    serializer = OrderDetailsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

