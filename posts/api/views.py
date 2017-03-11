from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
)
# Filters
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter)

# Pagination
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)
from .permissions import IsOwnerOrReadOnly

# Models
from posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def perform_create(self, serializer):
        """
        Gestiana la creación del articulo vinculado al usuario actual.
        :param serializer: objeto serializer de la del Modelos
        :return: Obejto de respuesta json son los datos
        """
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__first_name']
    pagination_class = PostPageNumberPagination # PostLimitOffsetPagination
