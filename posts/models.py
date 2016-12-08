# -*- coding:utf8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

from markdown_deux import markdown
from django.utils.safestring import mark_safe

from comments.models import Comment

from .utils import get_read_time

# Create your models here.

#Post.objects.all()
#Post.objects.create(user=user, title ='some title)

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    """
    Guarda las imagenes en un path (Uso instance.user)
    :param instance: objeto de la image
    :param filename: nombre del fichero
    :return: string de path de almacenamiento del archivo.
    """
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field=None,
                              height_field=None)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    read_time = models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()  # objects.all() por convencion se utiliza objects

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('url_post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp', '-updated']

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

# https://docs.djangoproject.com/en/1.10/ref/signals/
# Hacer algo antes de guardar la instacia
# Title Post 1 -> title-post-1
# Cambiar en view y url id por slug para que funcione.
# posts/title-post-1


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    post_qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = post_qs.exists()
    if exists:
        new_slug = '%s-%s' %(slug, post_qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.content:
        content_post = instance.get_markdown()
        read_time_var = get_read_time(content_post)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)