from django.conf.urls import url

# API Views
from .views import (
    CommentListAPIView,
    CommentDetailAPIView)


urlpatterns = [
    # API comment post URLs
    url(r'^$', CommentListAPIView.as_view(), name='list_api'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread_api'),
    #url(r'^(?P<pk>\d+)/delete/$', comment_delete, name='comment_delete_api'),

]
