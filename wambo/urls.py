# -*- coding:utf8 -*-
"""wambo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from users import urls as users_urls
from posts import urls as posts_urls
from comments import urls as comments_url

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Import Posts URLs
    url(r'^', include(posts_urls)),
    # Import Comments URLs
    url(r'^comments/', include(comments_url, namespace='comments')),
    # API comments URLs
    url(r'^api/comments/', include('comments.api.urls', namespace='comments-api')),
    # Import User URLs
    url(r'', include(users_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)