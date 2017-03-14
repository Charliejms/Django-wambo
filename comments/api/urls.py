from django.conf.urls import url

# API Views
from .views import (
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    CommentUpdateAPIView)


urlpatterns = [
    # API comment post URLs
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create_api'),
    url(r'^$', CommentListAPIView.as_view(), name='list_api'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread_api'),
    url(r'^(?P<pk>\d+)/update/$', CommentUpdateAPIView.as_view(), name='update_api'),

]
