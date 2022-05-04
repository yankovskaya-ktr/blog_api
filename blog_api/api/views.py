from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class PostViewSet(ListCreateViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@extend_schema_view(
    list=extend_schema(tags=['comments']),
    create=extend_schema(tags=['comments'])
)
class CommentViewSet(ListCreateViewSet):
    """
    Операции с комментариями в привязке к посту.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Получение комментариев до 3-его уровня вложенности
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.filter(level__lte=3).prefetch_related('children')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post)


@extend_schema_view(
    list=extend_schema(tags=['threads']),
    create=extend_schema(tags=['threads'])
)
class ThreadViewSet(ListCreateViewSet):
    """
    Операции с комментариями в привязке к родительскому комментарию.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Получение всех вложенных комментариев
        parent_id = self.kwargs.get('parent_id')
        parent = get_object_or_404(Comment, id=parent_id)
        return parent.get_descendants().prefetch_related('children')

    def perform_create(self, serializer):
        parent_id = self.kwargs.get('parent_id')
        parent = get_object_or_404(Comment, id=parent_id)
        post = parent.post
        serializer.save(post=post, parent=parent)
