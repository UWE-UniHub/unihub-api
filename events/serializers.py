from rest_framework import serializers
from .models import Event
from communities.serializers import CommunitySerializer , Community
from profiles.serializers import ProfileSerializer , Profile
from django.shortcuts import get_object_or_404

class EventSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    community = CommunitySerializer(read_only = True)
    profile = serializers.SerializerMethodField(read_only = True)


    class Meta:
        model = Event
        fields = ['id', 'description', 'location', 'created_at','date','profile','community']
        read_only_fields = ['id', 'created_at','community','profile']
    
    def get_profile(self,obj):
        if obj.community:
            return None
        return ProfileSerializer(obj.creator).data


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['description', 'location','date','creator_id', 'community_id']
