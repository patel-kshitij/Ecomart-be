from django.urls import path

from apps.application import views

''' Items Endpoints '''
urlpatterns = [
    path('add/', views.add_order, name='Create order'),
    path('shipping-address/', views.add_shipping_address, name='Add shipping address'),
    path('get-shipping-addresses/', views.get_shipping_addresses, name='Get shipping addresses'),
]
