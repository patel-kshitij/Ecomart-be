from django.urls import path

from apps.application import views

urlpatterns = [
    path('add_item/', views.add_shopping_cart_item, name='Add shopping cart item'),
    path('', views.shopping_cart_list, name='Shopping cart list'),
    path('delete/<int:cart_item_id>', views.shopping_cart_delete, name='Shopping cart delete'),
]
