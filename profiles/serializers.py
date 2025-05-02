from rest_framework import serializers
from profiles.models import Profile
from rest_framework.authtoken.models import Token
from communities.serializers import serializers_get_user_from_request

class ProfileSerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'date_of_birth', 'interests', 'bio', 'is_staff', 'subscribers', 'subscriptions', 'student', 'staff']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = serializers_get_user_from_request(self)

        if not (user and user.is_authenticated and str(user.id) == str(instance.id)):
            data.pop('address', None)
        return data

    def get_subscribers(self, obj):
        return obj.subscribers.count()

    def get_subscriptions(self, obj):
        return obj.subscriptions.count()

    def get_student(self, obj):
        if not obj.is_staff:
            return {
                "program": obj.program,
                "year": obj.year,
                "school": obj.school
            }
        return None

    def get_staff(self, obj):
        if obj.is_staff:
            return {
                "position": obj.position,
                "department": obj.department
            }
        return None
    
class ProfileDetailSerializer(ProfileSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ['is_subscribed']

    def get_is_subscribed(self, obj):
        user = serializers_get_user_from_request(self)
        return user.is_authenticated and obj.subscribers.filter(id=user.id).exists() if user else False