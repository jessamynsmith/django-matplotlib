from django.urls import path

from app import views


urlpatterns = [
    path('', views.ImageListView.as_view(), name='image_list'),
    path('create/', views.ImageCreateView.as_view(), name='image_create'),
    path('thumbnail/<int:pk>/', views.ThumbnailDetailView.as_view(), name='thumbnail_detail'),
    path('thumbnail/create/', views.ThumbnailCreateView.as_view(), name='thumbnail_create'),
]
