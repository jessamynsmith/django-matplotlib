from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.ImageListView.as_view(), name='image_list'),
    url(r'^create/$', views.ImageCreateView.as_view(), name='image_create'),
]
