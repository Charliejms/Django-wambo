from django.utils.timesince import timesince
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField)

# Models
from posts.models import Post


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish'
        ]

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:detail_api',
    lookup_field='pk'
)

post_delete_url = HyperlinkedIdentityField(
    view_name='posts-api:delete_api',
    lookup_field='pk'
)


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    image = SerializerMethodField()
    publish = SerializerMethodField()
    html = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'read_time',
            'image',
        ]

    @staticmethod
    def get_user(obj):
        return str(obj.user.username)

    @staticmethod
    def get_image(obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    @staticmethod
    def get_publish(obj):
        return timesince(obj.publish)

    @staticmethod
    def get_html(obj):
        return str(obj.get_markdown())


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'publish',
        ]

    def get_user(self, obj):
        return str(obj.user.username)

