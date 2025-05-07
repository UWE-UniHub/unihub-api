from rest_framework import serializers
from posts.views import check_user_can_pD_posts
from .models import Post
from communities.serializers import CommunitySerializer
from profiles.serializers import ProfileSerializer
from events.serializers import EventSerializer
from unihub.utils import serializers_get_user_from_request

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    community = CommunitySerializer(read_only = True)
    profile = ProfileSerializer(read_only = True)
    event = EventSerializer()

    likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'event', 'profile', 'community', 'tags', 'hidden', 'created_at','likes', 'is_liked', 'is_editable']
        read_only_fields = ['id', 'created_at', 'community', 'profile', 'likes', 'is_liked', 'is_editable']

    def get_likes(self,obj):
        return obj.likes.count()
    
    def get_is_liked(self,obj):
        user = serializers_get_user_from_request(self)
        return user.is_authenticated and obj.likes.filter(id=user.id).exists() if user else False
    
    def get_is_editable(self, obj):
        user = serializers_get_user_from_request(self)
        if not user or not user.is_authenticated:
            return False
        return check_user_can_pD_posts(user, obj)

class PostPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'event_id', 'tags', 'hidden']