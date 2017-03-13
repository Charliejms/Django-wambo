from django.conf.urls import url, include


from posts.views import post_create, post_detail, post_list, post_update, post_delete

urlpatterns = [
    # Web post URLs
    url(r'^$', post_list, name='url_post_list'),
    url(r'^create/$', post_create, name='url_post_create'),
    url(r'^(?P<pk>\d+)/$', post_detail, name='url_post_detail'),
    url(r'^(?P<pk>\d+)/update/$', post_update, name='url_post_update'),
    url(r'^(?P<pk>\d+)/delete/$', post_delete, name='url_post_delete'),

    # API post URLs
    url(r'^api/posts/', include('posts.api.urls', namespace='posts-api')),
]
