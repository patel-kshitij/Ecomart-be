from django.urls import path

from apps.application import views

''' Items Endpoints '''
urlpatterns = [
    path('add/', views.CreateItemView.as_view(), name='Create Item'),
    path('item-details/<int:item_id>/', views.item_detail_view, name='Item Detail'),
    path('delete/<int:item_id>/', views.item_delete_view, name='Delete Item'),
    path('update/<int:item_id>/', views.item_update_view, name='Update Item'),
    path('<int:page>', views.item_list_view_pagination, name='Item List With Page'),
    path('', views.item_list_view, name='Item List'),
    path('my-listings/', views.my_listings_view, name='My Listings'),
    path('add-images/<int:item_id>/', views.item_image_add_view, name='Add Images'),
    path('update-images/<int:item_id>/', views.item_image_update_view, name='Update Images'),
]


''' Bidding Endpoints '''
urlpatterns += [
    path('bids/add', views.add_bid_item_view, name='Add Bid Item'),
    path('bids/delete/<int:item_bid_id>/', views.delete_bid_item_view, name='Delete Bid Item'),
    path('bids/<int:item_id>/', views.get_bid_item_view, name='List Item bids'),
]
