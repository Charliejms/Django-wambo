from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
)

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

# Permissions to Post
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

# Models
from comments.models import Comment

# Serializer
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    create_comment_serializer)


class CommentCreateAPIView(CreateAPIView):
    # Comments
    # POST /api/comments/create/?type=post&pk=Post.id
    # Replies
    # POST /api/comments/create/?type=post&pk=Post.id&parent_id=Comment.id
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        pk = self.request.GET.get('pk')
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(model_type=model_type,
                                         pk=pk,
                                         parent_id=parent_id,
                                         user=self.request.user)


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list
