from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import ItemModel
from ..serializers import ItemSerializer, ItemDetailsSerializer


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
    item.save()

    serializer = ItemDetailsSerializer(item)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list_view(request):
    try:
        items = ItemModel.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except ItemModel.DoesNotExist:
        return Response(data={'message': 'Item does not exist',
                              'status': False})
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
