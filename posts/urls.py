from django.conf.urls import url
from django.contrib import admin

from posts.views import post_home, post_create, post_detail, post_list, post_update, post_delete

urlpatterns = [
    # Web post URLs
    url(r'^$', post_list, name='url_post_list'),
    url(r'^create/$', post_create, name='url_post_create'),
    url(r'^(?P<pk>\d+)/$', post_detail, name='url_post_detail'),
    url(r'^(?P<pk>\d+)/update/$', post_update, name='url_post_update'),
    url(r'^delete/$', post_delete, name='url_post_delete'),

    # API post URLs
]
