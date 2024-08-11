from django.urls import path

from apps.application import views

urlpatterns = [
    path('add_item/', views.add_wishlist_item, name='Add Wishlist item'),
    path('', views.wishlist_list, name='Wishlist list'),
    path('delete/<int:wishlist_id>', views.wishlist_delete, name='Wishlist delete'),
]
