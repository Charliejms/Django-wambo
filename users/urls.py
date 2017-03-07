# -*- coding:utf8 -*-from django.conf.urls import url, include
from django.conf.urls import url

from users.views import login_view, logout_view, register_view

urlpatterns = [
    # Web URLS
    #url(r'^login$', LoginView.as_view(), name='users_login'),
    #url(r'^logout$', LogoutView.as_view(), name='users_logout'),
    #url(r'^register$', RegisterView.as_view(), name='users_register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    # API URLS
 ]