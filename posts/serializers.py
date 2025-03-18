from rest_framework import serializers
from .models import Post
from communities.serializers import CommunitySerializer
from profiles.serializers import ProfileSerializer
from events.serializers import EventSerializer

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    community = CommunitySerializer(read_only = True)
    profile = ProfileSerializer(read_only = True)
    event = EventSerializer()

    class Meta:
        model = Post
        fields = ['id', 'content', 'event','profile','community', 'created_at']
        read_only_fields = ['id', 'created_at','community','profile']

class PostPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'event_id']