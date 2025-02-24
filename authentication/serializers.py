from rest_framework import serializers
from profiles.models import Profile

class StudentSerializer(serializers.Serializer):
    program = serializers.CharField(required=True)
    level = serializers.CharField(required=True)
    school = serializers.CharField(required=True)

class StaffSerializer(serializers.Serializer):
    position = serializers.CharField(required=True)
    department = serializers.CharField(required=True)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    student = StudentSerializer(required=False)
    staff = StaffSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'password', 'is_staff', 'student', 'staff']

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)
        
        student_data = validated_data.pop('student', None)
        staff_data = validated_data.pop('staff', None)

        if is_staff:
            student_data = None
        else:
            staff_data = None

        user = Profile.objects.create(is_staff=is_staff, **validated_data)

        if student_data:
            user.program = student_data['program']
            user.level = student_data['level']
            user.school = student_data['school']
        if staff_data:
            user.position = staff_data['position']
            user.department = staff_data['department']

        user.set_password(validated_data['password'])
        user.save()
        return user
