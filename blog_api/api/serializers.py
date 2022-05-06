from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text')
        model = Post


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'post', 'level', 'parent', 'children')
        read_only_fields = ('post', 'level', 'parent', 'children')
        model = Comment


class CommentListSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'post', 'level', 'parent', 'children')
        read_only_fields = ('post', 'level', 'parent', 'children')
        model = Comment

    def get_children(self, obj):
        children = self.context['children'].get(obj.id, [])
        serializer = CommentListSerializer(
            children, many=True, context=self.context)
        return serializer.data
