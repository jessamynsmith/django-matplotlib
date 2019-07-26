from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.ImageListView.as_view(), name='image_list'),
    url(r'^create/$', views.ImageCreateView.as_view(), name='image_create'),
    url(r'^thumbnail/(?P<pk>[0-9]+)/$', views.ThumbnailDetailView.as_view(), name='thumbnail_detail'),
    url(r'^thumbnail/create/$', views.ThumbnailCreateView.as_view(), name='thumbnail_create'),
]
