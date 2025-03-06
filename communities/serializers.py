from rest_framework import serializers
from communities.models import Community
from profiles.serializers import ProfileSerializer
from rest_framework.authtoken.models import Token

class CommunitySerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()
    

    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'subscribers']

    def get_subscribers(self, obj):
        return obj.subscribers.count()
    
class CommunityDetailSerializer(CommunitySerializer):
    is_admin = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()

    class Meta(CommunitySerializer.Meta):
        fields = CommunitySerializer.Meta.fields + ['is_admin', 'is_creator']

    def get_is_admin(self, obj):
        request = self.context.get('request')
        token = request.COOKIES.get('token')
        user = Token.objects.get(key=token).user
        if user and user.is_authenticated:
            return obj.admins.filter(id=user.id).exists()
        return False

    def get_is_creator(self, obj):
        request = self.context.get('request')
        token = request.COOKIES.get('token')
        user = Token.objects.get(key=token).user
        if user and user.is_authenticated:
            return obj.creator == user
        return False


class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'bio', 'creator_id']
    