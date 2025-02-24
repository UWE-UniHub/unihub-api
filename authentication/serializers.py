from rest_framework import serializers
from profiles.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Profile
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = Profile.objects.create(
            id=validated_data['id'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
