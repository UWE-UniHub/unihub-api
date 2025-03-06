import os
from django.conf import settings
from django.http import FileResponse
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from unihub.settings import AVATAR_DIR

def get_user_from_request(request):
    token = request.COOKIES.get("token")

    if not token:
        return None, Response({"error": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = Token.objects.get(key=token).user
        return user, None
    except Token.DoesNotExist:
        return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PATCH', 'DELETE'])
def profile_detail(request, id):
    profile = get_object_or_404(Profile, id=id)

    if request.method in ['PATCH', 'DELETE']:
        user, error_response = get_user_from_request(request)
        if error_response:
            return error_response
        if not user or user.id != profile.id:
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        profile.delete()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def profile_avatar(request, id):
    profile = get_object_or_404(Profile, id=id)
    avatar_path = os.path.join(AVATAR_DIR, f"{id}.png")
    if request.method in ['PUT', 'DELETE']:
        user, error_response = get_user_from_request(request)
        if error_response:
            return error_response
        if not user or user.id != profile.id:
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if os.path.exists(avatar_path):
            return FileResponse(open(avatar_path, 'rb'), content_type='image/png')
        return Response({"error": "Avatar not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        if not request.body:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with open(avatar_path, 'wb') as f:
                f.write(request.body)
            return Response({"message": "Avatar uploaded successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to save avatar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
            return Response({"message": "Avatar deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Avatar not found"}, status=status.HTTP_404_NOT_FOUND)    
    
@api_view(['GET'])
def profile_followers(request, id):
    profile = get_object_or_404(Profile, id=id)
    subscribers = profile.subscribers.all()
    serializer = ProfileSerializer(subscribers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def profile_subscriptions(request, id):
    profile = get_object_or_404(Profile, id=id)
    subscriptions = profile.subscriptions.all()
    serializer = ProfileSerializer(subscriptions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])
def add_delete_prof_subs(request, id):
    profile = get_object_or_404(Profile, id=id)
    
    user_id, error_response = get_user_from_request(request)
    user_id = user_id.id
    
    if error_response:
        return error_response
    
    if request.method == 'POST':
        subscriber = get_object_or_404(Profile, id=user_id)
        profile.subscribers.add(subscriber)
        return Response({"message": "Subscribed successfully"}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        subscriber = get_object_or_404(Profile, id=user_id)
        profile.subscribers.remove(subscriber)
        return Response({"message": "Unsubscribed successfully"}, status=status.HTTP_204_NO_CONTENT)
