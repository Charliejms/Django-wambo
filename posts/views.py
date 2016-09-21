# -*- coding:utf8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from posts.form import PostForm
from posts.models import Post


def post_home(request):
    return HttpResponse("<h1>Hola</h1>")


def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        'form': form,
        'title': 'Post Form',
    }
    return render(request, 'posts/post_form.html', context)


def post_detail(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    context = {
        'title': instance.title,
        'instance': instance
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    post_qs = Post.objects.all()
    context = {
        'object_list': post_qs,
        'title': 'List Post'
    }
    return render(request, 'posts/list_posts.html', context)


def post_update(request, pk):

    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance= instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'posts/post_form.html', context)


def post_delete(request):

    return HttpResponse("<h1>Delete</h1>")
