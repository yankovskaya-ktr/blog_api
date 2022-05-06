from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .models import Comment, Post
from .serializers import (CommentCreateSerializer, CommentListSerializer,
                          PostSerializer)


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


@extend_schema_view(
    list=extend_schema(description='Получить все посты', tags=['posts']),
    create=extend_schema(description='Создать пост', tags=['posts'])
)
class PostViewSet(ListCreateViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@extend_schema_view(
    list=extend_schema(
        description='Получить комментарии к посту до 3-его уровня вложенности',
        tags=['comments']
    ),
    create=extend_schema(description='Создать комментарий к посту',
                         tags=['comments'])
)
class CommentViewSet(ListCreateViewSet):
    """
    Операции с комментариями в привязке к посту.
    """
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        return CommentCreateSerializer

    def list(self, request, *args, **kwargs):
        # Получение комментариев до 3-его уровня вложенности
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        queryset = post.comments.filter(
            level__lte=2).prefetch_related('children')

        children = {comment.pk: comment.children for comment in queryset}

        serializer = self.get_serializer(
            post.comments.filter(level__lte=0),
            many=True,
            context={'children': children}
        )
        return Response(serializer.data)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post)


@extend_schema_view(
    list=extend_schema(
        description='Получить все вложенные комментарии для родительского',
        tags=['threads']
    ),
    create=extend_schema(description='Ответить на комментарий',
                         tags=['threads'])
)
class ThreadViewSet(ListCreateViewSet):
    """
    Операции с комментариями в привязке к родительскому комментарию.
    """
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        return CommentCreateSerializer

    def list(self, request, *args, **kwargs):
        # Получение всех вложенных комментариев
        parent_id = self.kwargs.get('parent_id')
        parent = get_object_or_404(Comment, id=parent_id)
        queryset = parent.get_descendants().prefetch_related('children')

        children = {comment.pk: comment.children for comment in queryset}

        serializer = self.get_serializer(
            parent.get_children(),
            many=True,
            context={'children': children}
        )
        return Response(serializer.data)

    def perform_create(self, serializer):
        parent_id = self.kwargs.get('parent_id')
        parent = get_object_or_404(Comment, id=parent_id)
        post = parent.post
        serializer.save(post=post, parent=parent)
