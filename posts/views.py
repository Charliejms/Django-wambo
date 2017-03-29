# -*- coding:utf8 -*-
from urllib.parse import quote_plus

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

# Create your views here.
from posts.form import PostForm
from posts.models import Post
from comments.forms import CommentForm
from comments.models import Comment


def post_home(request):
    return HttpResponse("<h1>Hola</h1>")


@login_required
def post_create(request):
    """
    Gestiona la creación de un aritculo del blog
    :param request: Objeto Htttprequest con los parametros de la petición
    :return: objeto Httpresponse con los parametros de respuesta
    """
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
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
    """
    Gestiona los detalles de los articulos del post
    :param request: objeto HttpRequiest con los datos de la petición
    :param pk: parametro identificador del articulo publicado
    :return: objeto HttpResponse con los datos de la respuesta
    """
    instance = get_object_or_404(Post, pk=pk)
    if instance.publish > timezone.now() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.title)

    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = request.POST.get('parent_id')
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url());



    #commets in post
    comments = instance.comments #Comment.objects.filter_by_instance(instance)
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'posts/post_detail.html', context)


def post_list(request):
    """
    Gestiona la lista de articulos de blog publicados sin incluir los draft (borradores)
    :param request: objeto HttpRequest con los datos de la petición
    :return: objeto HttpResponse con los datos de la respuesta.
    """
    today = timezone.now()
    post_qs_list = Post.objects.active() #.order_by('-timestamp')
    # Mira todo los post si incluidos los draft
    if request.user.is_staff or request.user.is_superuser:
        post_qs_list = Post.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        post_qs_list = post_qs_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        ).distinct()
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
        'today': today,
    }
    return render(request, 'posts/list_posts.html', context)


def post_update(request, pk):
    """
    Gestiona la actualización de un articulo del blog
    :param request: objeto Httprequest con los datos de la petición
    :param pk: parametro que identifica un articulo del blog
    :return: objeto HttpResponse con los datos de la respuesta
    """
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
    """
    Gestiona el borrado de un articulo del blog.
    :param request: objeto HttpRequest con los datos de la petición
    :param pk: parametro que identifica el aticulo del blog
    :return: objeto HttpResponse con los datos de la respuesta
    """
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    instance.delete()
    messages.success(request, 'Post Successfully Deleted')
    return redirect('url_post_list')



