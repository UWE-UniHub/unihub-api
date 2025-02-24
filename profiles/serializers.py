from rest_framework import serializers
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    subscribers = serializers.SerializerMethodField()
    subscriptions = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    staff = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'bio', 'is_staff', 'subscribers', 'subscriptions', 'student', 'staff']

    def get_subscribers(self, obj):
        return obj.subscribers.count()

    def get_subscriptions(self, obj):
        return obj.subscriptions.count()

    def get_student(self, obj):
        if not obj.is_staff:
            return {
                "program": obj.program,
                "level": obj.level,
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
