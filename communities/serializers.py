from rest_framework import serializers
from communities.models import Community

class CommunitySerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()
    

    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'subscribers']

    def get_subscribers(self, obj):
        return obj.subscribers.count()
    
class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'creator_id']
    