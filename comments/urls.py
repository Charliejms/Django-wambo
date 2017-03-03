from django.conf.urls import url

from comments.views import comment_thread, comment_delete

urlpatterns = [
    # Web comment post URLs
    url(r'^(?P<pk>\d+)/$', comment_thread, name='url_comment_thread'),
    url(r'^(?P<pk>\d+)/delete/$', comment_delete, name='url_comment_delete'),

]
