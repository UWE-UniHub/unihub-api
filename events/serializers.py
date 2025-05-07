from rest_framework import serializers
from unihub.utils import serializers_get_user_from_request
from .models import Event
from communities.serializers import CommunitySerializer
from profiles.serializers import ProfileSerializer

class EventSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    community = CommunitySerializer(read_only = True)
    profile = serializers.SerializerMethodField(read_only = True)
    subscribers_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    is_deletable = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'description', 'location', 'created_at', 'date', 'profile', 'community', 'required_materials', 'max_capacity', 'subscribers_count', 'is_subscribed', 'is_deletable']
        read_only_fields = ['id', 'created_at', 'community', 'profile', 'subscribers_count', 'is_subscribed', 'is_deletable']
    
    def get_profile(self,obj):
        if obj.community:
            return None
        return ProfileSerializer(obj.creator).data
    
    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_is_subscribed(self, obj):
        user = serializers_get_user_from_request(self)
        if not user or not user.is_authenticated:
            return False
        return obj.subscribers.filter(id=user.id).exists()
    
    def get_is_deletable(self, obj):
        user = serializers_get_user_from_request(self)
        if not user or not user.is_authenticated:
            return False

        if obj.creator_id == user.id and obj.community is None:
            return True

        if obj.community:
            if obj.community.creator_id == user.id:
                return True
            if obj.community.admins.filter(id=user.id).exists():
                return True
        return False

class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['description', 'location', 'date', 'creator_id', 'community_id', 'required_materials', 'max_capacity']
