from django.urls import path

from apps.application import views

''' Items Endpoints '''
urlpatterns = [
    path('', views.get_orders, name='Get orders'),
    path('add/', views.add_order, name='Create order'),
    path('shipping-address/', views.add_shipping_address, name='Add shipping address'),
    path('get-shipping-addresses/', views.get_shipping_addresses, name='Get shipping addresses'),
    path('shipping-address/update/<int:shipping_address_id>/', views.update_shipping_address,
         name='Update shipping address'),
    path('update/<int:order_id>/', views.update_order_details, name='Update order'),
]
