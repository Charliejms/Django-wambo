# -*- coding:utf8 -*-from django.conf.urls import url, include
from django.conf.urls import url, include

from users.views import login_view, logout_view, register_view

urlpatterns = [
    # Web URLS
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    # API URLS
    url(r'^api/users/', include('users.api.urls', namespace='user-api')),
 ]
