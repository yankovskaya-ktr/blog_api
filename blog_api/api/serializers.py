from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text')
        model = Post


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'post', 'parent', 'children', 'level')
        read_only_fields = ('post', 'parent', 'children', 'level')
        model = Comment
