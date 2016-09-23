# -*- coding:utf8 -*-
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


def upload_location(instance, filename):
    """
    Guarda las imagenes en un path (Uso instance.user)
    :param instance: objeto de la image
    :param filename: nombre del fichero
    :return: string de path de almacenamiento del archivo.
    """
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field=None,
                              height_field=None)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('url_post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp', '-updated']