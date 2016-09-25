# -*- coding:utf8 -*-
from urllib.parse import quote_plus

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from posts.form import PostForm
from posts.models import Post


def post_home(request):
    return HttpResponse("<h1>Hola</h1>")


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, 'Post Successfully Created')
        return redirect('url_post_detail', pk=instance.pk)
    # else:
    #     messages.error(request, 'Post  NOT Successfully Created')
    context = {
        'form': form,
        'title': 'Post Form',
    }
    return render(request, 'posts/post_form.html', context)


def post_detail(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    share_string = quote_plus(instance.title)
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    post_qs_list = Post.objects.all() #.order_by('-timestamp')
    paginator = Paginator(post_qs_list, 5)  # Show 25 contacts per page
    page_rqs_var = 'page'
    page = request.GET.get(page_rqs_var)
    try:
        post_qs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_qs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_qs = paginator.page(paginator.num_pages)
    context = {
        'object_list': post_qs,
        'title': 'List Post',
        'page_rqs_var': page_rqs_var,
    }
    return render(request, 'posts/list_posts.html', context)


def post_update(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post Save', extra_tags='update-post')
        return redirect('url_post_detail', pk=instance.pk)
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'posts/post_form.html', context)


def post_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    instance.delete()
    messages.success(request, 'Post Successfully Deleted')
    return redirect('url_post_list')



