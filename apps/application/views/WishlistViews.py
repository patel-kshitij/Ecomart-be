from django.core.paginator import Paginator
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import ItemModel, ItemImagesModel, ItemBidModel, WishlistModel
from ..serializers import ItemSerializer, ItemDetailsSerializer
from ..serializers.WishlistSerializer import WishlistSerializer
from ...accounts.models import UserModel
from ...accounts.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_wishlist_item(request):
    try:
        user_id = request.user.id
        item_id = request.data['item_id']

        try:
            list_item = WishlistModel.objects.get(user_id=user_id, item_id=item_id)
            list_item.save()

        except WishlistModel.DoesNotExist:
            WishlistModel.objects.create(user_id=user_id, item_id=item_id)
        return Response(status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_list(request):
    try:
        user_id = request.user.id
        cart = WishlistModel.objects.filter(user_id=user_id)
        serializer = WishlistSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def wishlist_delete(request, cart_item_id):
    try:
        user_id = request.user.id
        WishlistModel.objects.get(id=cart_item_id, user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except WishlistModel.DoesNotExist:
        return Response(data={'error': 'Cart item does not exist'}, status=status.HTTP_400_BAD_REQUEST)
