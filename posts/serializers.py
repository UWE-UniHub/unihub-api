from rest_framework import serializers
from .models import Post
from profiles.serializers import ProfileSerializer
from communities.serializers import CommunitySerializer

class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(allow_null=True)
    community = CommunitySerializer(allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'event_id', 'profile', 'community']
        read_only_fields = ['id', 'created_at', 'profile', 'community']