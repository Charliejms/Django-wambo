from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,)
from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
)

# Permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

# Permissions to Post and Pagination
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

# Models
from comments.models import Comment

# Serializer
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    #CommentUpdateSerializer,
    create_comment_serializer,)


class CommentCreateAPIView(CreateAPIView):
    # Comments
    # POST /api/comments/create/?type=post&pk=Post.id
    # Replies
    # POST /api/comments/create/?type=post&pk=Post.id&parent_id=Comment.id
    queryset = Comment.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        pk = self.request.GET.get('pk')
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(model_type=model_type,
                                         pk=pk,
                                         parent_id=parent_id,
                                         user=self.request.user)


# class CommentUpdateAPIView(RetrieveAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetailSerializer


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        # PUT method Http
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # DELETE method Http
        return self.delete(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list
