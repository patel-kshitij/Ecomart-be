from django.urls import path, include

from .views import UserDetailsView

''' Items Endpoints '''
urlpatterns = [
    path('items/', include('apps.application.application_urls.ItemsUrls'), name='Item Urls'),
    # path('delete-item')
]

''' Category Endpoints '''
urlpatterns += [
    path('categories/', include('apps.application.application_urls.CategoryUrls'), name='Category Urls'),
]

''' User details Endpoints '''
urlpatterns += [
    path('user/', UserDetailsView.as_view(), name='User Details'),
]

''' Orders Endpoints '''
urlpatterns += [
    path('order/', include('apps.application.application_urls.OrdersUrls'), name='Order Urls'),
]

''' Cart Endpoints '''
urlpatterns += [
    path('cart/', include('apps.application.application_urls.ShoppingCartUrls'), name='Cart Urls'),
]

''' Wishlists Endpoints '''
urlpatterns += [
    path('wishlist/', include('apps.application.application_urls.WishlistUrls'), name='Wishlist Urls'),
]
