from django.urls import path

from apps.application import views

''' Category Endpoints '''
urlpatterns = [
    path('add/', views.CreateCategoryView.as_view(), name='Create Category'),
    path('<int:category_id>/', views.category_detail_view, name='Category Detail'),
    path('delete/<int:category_id>/', views.category_delete_view, name='Delete Category'),
    path('', views.category_list_view, name='Category List'),
]
