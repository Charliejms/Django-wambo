# -*- coding:utf8 -*-from django.conf.urls import url, include
from django.conf.urls import url, include

from .views import (UserCreateAPIView,
                    UserLoginAPIView)

urlpatterns = [
    # Users API URLS
    url(r'^login/$', UserLoginAPIView.as_view(), name='login-api'),
    url(r'^logout/$', UserCreateAPIView.as_view(), name='logout-api'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register-api'),
]
