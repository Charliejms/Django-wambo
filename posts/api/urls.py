from django.conf.urls import url

#API views
from posts.api.views import (PostListAPIView,
                             PostDetailAPIView,
                             PostDeleteAPIView,
                             PostUpdateAPIView,
                             PostCreateAPIView)


urlpatterns = [
    # API post URLs
    url(r'^$', PostListAPIView.as_view(), name='list_api'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create_api'),
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail_api'),
    url(r'^(?P<pk>\d+)/update/$', PostUpdateAPIView.as_view(), name='update_api'),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteAPIView.as_view(), name='delete_api'),

]
