from rest_framework import serializers
from communities.models import Community
from unihub.utils import serializers_get_user_from_request

class CommunitySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    subscribers = serializers.SerializerMethodField()
    

    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'tags', 'subscribers']
        read_only_fields = ['id']

    def get_subscribers(self, obj):
        return obj.subscribers.count()
    
class CommunityDetailSerializer(CommunitySerializer):
    is_admin = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta(CommunitySerializer.Meta):
        fields = CommunitySerializer.Meta.fields + ['is_admin', 'is_creator', 'is_subscribed']

    def get_is_admin(self, obj):
        user = serializers_get_user_from_request(self)
        if user and user.is_authenticated:
            return obj.admins.filter(id=user.id).exists()
        return False

    def get_is_creator(self, obj):
        user = serializers_get_user_from_request(self)
        if user and user.is_authenticated:
            return obj.creator == user
        return False
    
    def get_is_subscribed(self, obj):
        user = serializers_get_user_from_request(self)
        if user and user.is_authenticated:
            return obj.subscribers.filter(id=user.id).exists()
        return False


class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'tags', 'creator_id']
    