from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_profile_by_id(request, id):
    profile = get_object_or_404(Profile, id=id)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def edit_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response({"error": "profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(profile, request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        profile.delete()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)