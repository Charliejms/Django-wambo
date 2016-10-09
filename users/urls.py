# -*- coding:utf8 -*-from django.conf.urls import url, include
from django.conf.urls import url
from users.views import LoginView, LogoutView

urlpatterns = [
    # Web URLS
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),
    #url(r'^register$', RegisterView.as_view(), name='users_register'),
    # API URLS
]