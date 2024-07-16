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
