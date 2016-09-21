# -*- coding:utf8 -*-
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absotute_url(self):
        return reverse('url_post_detail', kwargs={'pk': self.pk})
