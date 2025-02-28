from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

def get_user_id_from_token(request):
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
        user, error_response = get_user_id_from_token(request)
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
    print(10)
    profile = get_object_or_404(Profile, id=str(id))
    user_id, error_response = get_user_id_from_token(request)
    
    if error_response:
        print(1)
        return error_response
    
    if request.method == 'POST':
        subscriber = get_object_or_404(Profile, id=str(user_id))
        profile.subscribers.add(subscriber)
        return Response({"message": "Subscribed successfully"}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        subscriber = get_object_or_404(Profile, id=str(user_id))
        profile.subscribers.remove(subscriber)
        return Response({"message": "Unsubscribed successfully"}, status=status.HTTP_204_NO_CONTENT)
