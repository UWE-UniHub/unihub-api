from rest_framework import serializers
from communities.models import Community
from profiles.serializers import ProfileSerializer

class CommunitySerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()
    creator = ProfileSerializer()
    admins = ProfileSerializer(many=True)

    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'creator', 'admins','subscribers']

    def get_subscribers(self, obj):
        return obj.subscribers.count()
    
class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'creator_id']
    