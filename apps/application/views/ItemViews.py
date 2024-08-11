from django.core.paginator import Paginator
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import ItemModel, ItemImagesModel, ItemBidModel
from ..serializers import ItemSerializer, ItemDetailsSerializer
from ...accounts.models import UserModel
from ...accounts.serializers import UserSerializer


class CreateItemView(generics.CreateAPIView):
    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_detail_view(request, item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
        serializer = ItemDetailsSerializer(item)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist',
                              'status': False
                              }, status=status.HTTP_404_NOT_FOUND, )

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def item_delete_view(request, item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist',
                              'status': False
                              }, status=status.HTTP_404_NOT_FOUND, )
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def item_update_view(request, item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist',
                              'status': False
                              }, status=status.HTTP_404_NOT_FOUND, )

    item.name = request.data['name']
    item.description = request.data['description']
    item.price = request.data['price']
    item.condition = request.data['condition']
    item.is_bidding_enabled = request.data['is_bidding_enabled']
    item.is_sold = request.data['is_sold']
    item.save()

    serializer = ItemDetailsSerializer(item)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list_view(request):
    try:
        user_id = request.user.id
        items = ItemModel.objects.all().exclude(is_sold=True).exclude(seller_id=user_id).order_by('-createdAt')

        serializer = ItemDetailsSerializer(items, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_listings_view(request):
    try:
        user_id = request.user.id
        items = ItemModel.objects.filter(seller_id=user_id).order_by('-createdAt')
        serializer = ItemDetailsSerializer(items, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list_view_pagination(request, page):
    try:
        items = ItemModel.objects.all()

        page = int(page)
        pages = Paginator(items, 20)
        pageNObjects = pages.page(page)
        maxPages = pages.num_pages

        serializer = ItemDetailsSerializer(pageNObjects.object_list, many=True)

        context = {
            'items': serializer.data,
            'max_pages': maxPages,
            'current_page': page,
        }
        return Response(data=context, status=status.HTTP_200_OK)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist',
                              'status': False})
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def item_image_add_view(request, item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
        images = request.data['images']
        for image in images:
            ItemImagesModel.objects.create(item=item, image=image)
        return Response(status=status.HTTP_201_CREATED)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def item_image_update_view(request, item_id):
    try:
        item = ItemModel.objects.get(id=item_id)
        images = request.data['images']
        ItemImagesModel.objects.filter(item=item).delete()
        for image in images:
            ItemImagesModel.objects.create(item=item, image=image)
        return Response(data={'message': 'Images Updated'},status=status.HTTP_200_OK)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bid_item_view(request):
    try:
        user_id = request.user.id
        item_id = int(request.data['item_id'])
        bid_amount = float(request.data['bid'])
        try:
            item = ItemModel.objects.get(id=item_id)
            if not item.is_bidding_enabled:
                return Response(data={'message': 'Item bidding is not enabled'}, status=status.HTTP_400_BAD_REQUEST)
        except ItemModel.DoesNotExist:
            return Response(data={'message': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            UserModel.objects.get(id=user_id)
            if user_id == item.seller_id:
                return Response(data={'message': 'Seller cannot bid on their own item'},)
        except UserModel.DoesNotExist:
            return Response(data={'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        ItemBidModel.objects.create(item_id=item_id, bid_amount=bid_amount, user_id=user_id)
        return Response(data={'message': 'Bid Placed'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_bid_item_view(request, item_bid_id):
    try:
        ItemBidModel.objects.get(id=item_bid_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    except ItemBidModel.DoesNotExist:
        return Response(data={'message': 'Bid does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bid_item_view(request, item_id):
    try:
        bids_object = ItemBidModel.objects.filter(item_id=item_id)

        bids = []

        for bid in bids_object:
            bids.append({
                'id': bid.item_id,
                'user': UserSerializer(bid.user).data,
                'amount': bid.bid_amount
            })

        return Response(data={'bids': bids}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
