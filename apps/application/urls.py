from django.urls import path, include
from .views import CreateItemView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserDetailsView

''' Items Endpoints '''
urlpatterns = [
    path('items/', include('apps.application.application_urls.ItemsUrls'), name='Create Item'),
    # path('delete-item')
]

''' User details Endpoints '''
urlpatterns += [
    path('user/', UserDetailsView.as_view(), name='User Details'),
]
