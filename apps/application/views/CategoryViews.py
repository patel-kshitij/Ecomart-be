from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import CategoryModel
from ..serializers import CategorySerializer


class CreateCategoryView(generics.CreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail_view(request, category_id):
    try:
        category = CategoryModel.objects.get(id=category_id)
        serializer = CategorySerializer(category)
    except CategoryModel.DoesNotExist:
        return Response(data={
            'message': 'Category does not exist',
            'status': False
        }, status=status.HTTP_404_NOT_FOUND, )

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_delete_view(request, category_id):
    try:
        category = CategoryModel.objects.get(id=category_id)
    except CategoryModel.DoesNotExist:
        return Response(data={
            'message': 'Category does not exist',
            'status': False
        }, status=status.HTTP_404_NOT_FOUND, )
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list_view(request):
    try:
        category = CategoryModel.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except CategoryModel.DoesNotExist:
        return Response(data={
            'message': 'Category does not exist',
            'status': False
        })
    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
