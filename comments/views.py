from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


# Create your views here.
from .models import Comment
from .forms import CommentForm


@login_required  # Settings
def comment_delete(request, pk):
    """
    Gestiona el borrado de comentarios de un articulo del blog
    :param request: objeto HttpRequesst con los datos de la petición
    :param pk: parametro que identifica un comentario para su eliminación
    :return: obejto HttoResponse con los datos de la respuesta.
    """
    try:
        obj = Comment.objects.get(pk=pk)
    except:
        Http404
    if obj.user != request.user:
        #messages.success(request, "You do not have permission to do this.")
        #raise Http404
        response = HttpResponse("You do ot have permission  to do this")
        response.status_code = 403
        return response
        #return render(request, 'comment_delete.html', context, status_code= 403)

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This comment has been deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        'object': obj
    }

    return render(request, 'comment_delete.html', context)


def comment_thread(request, pk):
    """
    Gestiona la lista de comentarios realcionados
    :param request: obejto HttpRequest con los datos de la petición
    :param pk: parametro para identificar si se trata de un comentario padre dentro lista
    :return: obejto HttpResponse con los datos de la respuesta
    """
    try:
        obj = Comment.objects.get(pk=pk)
    except:
        Http404

    if not obj.is_parent:
        obj = obj.parent

    initial_data = {
        'content_type': obj.content_type,
        'object_id': obj.object_id,
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
    context = {
        "comment": obj,
        "comment_form": form,
    }
    return render(request, "comment.html", context)