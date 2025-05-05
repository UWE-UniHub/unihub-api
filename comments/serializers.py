from rest_framework import serializers
from .models import Comment
from profiles.serializers import ProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    author_id = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'post']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
