import os
from django.conf import settings
from django.http import FileResponse
from unihub.utils import validate_png
from .models import Community
from profiles.models import Profile
from .serializers import CommunitySerializer, CommunityPostSerializer, CommunityDetailSerializer
from profiles.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from profiles.views import get_user_from_request
from unihub.settings import COMMUNITY_AVATAR_DIR

def check_user_is_admin(user, community):
    return community.admins.filter(id=user.id).exists()

def check_user_is_community_creator(user, community):
    return community.creator == user

@api_view(['GET','POST'])
def communitiesGetPost(request):   

    user, error_response = get_user_from_request(request)

    if request.method == 'GET':
        serializer = CommunitySerializer(Community.objects.all(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:

        if error_response:
            return error_response
        
        serializer = CommunityPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['creator_id'] = user.id
            serializer.save()
            community = get_object_or_404(Community,id=serializer.data['id'])
            community.admins.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH','DELETE'])
def communitiesGetPatchDelete(request,id):
    community = get_object_or_404(Community, id = id)
    if request.method =='GET':
        serializer = CommunityDetailSerializer(community, context={'request': request, 'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response
        
    if request.method =='PATCH':
        if not check_user_is_admin(user, community) and not check_user_is_community_creator(user, community):
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommunitySerializer(community, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        if not check_user_is_community_creator(user, community):
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        community.delete()
        return Response({"message": "Community deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def community_subscribers(request,id):
    community = get_object_or_404(Community, id=id)
    subscribers = community.subscribers.all()
    serializer = ProfileSerializer(subscribers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST','DELETE'])
def add_delete_comm_subs(request,id):
    community = get_object_or_404(Community, id=id)
    user, error_response = get_user_from_request(request)

    if error_response:
        return error_response
    
    user = user.id

    if request.method == 'POST':
        community.subscribers.add(user)
        return Response({"message": "Subscribed successfully"}, status=status.HTTP_200_OK)
    else:
        community.subscribers.remove(user)
        return Response({"message": "Unsubscribed successfully"}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT', 'DELETE'])
def community_avatar(request, id):
    community = get_object_or_404(Community, id=id)
    avatar_path = os.path.join(COMMUNITY_AVATAR_DIR, f"{community.id}.png")

    if request.method in ['PUT', 'DELETE']:
        user, error_response = get_user_from_request(request)
        if error_response:
            return error_response
        if not check_user_is_admin(user, community) and not check_user_is_community_creator(user, community):
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if os.path.exists(avatar_path):
            return FileResponse(open(avatar_path, 'rb'), content_type='image/png')
        return Response({"error": "Avatar not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        if not request.body:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        is_png, error_message = validate_png(request.body)
        if not is_png:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
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
def community_admins(request, id):
    community = get_object_or_404(Community, id=id)
    creator = community.creator
    admins = community.admins.exclude(id=creator.id)
    creator_serializer = ProfileSerializer(creator)
    admins_serializer = ProfileSerializer(admins, many=True)
    return Response({"creator": creator_serializer.data, "admins": admins_serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])
def add_delete_admin(request, community_id, admin_id):
    community = get_object_or_404(Community, id=community_id)
    user, error_response = get_user_from_request(request)

    if error_response:
        return error_response
    
    if not check_user_is_community_creator(user, community):
            return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        new_admin = get_object_or_404(Profile, id=admin_id)
        community.admins.add(new_admin)
        return Response({"message": "Admin added successfully"}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        delete_admin = get_object_or_404(Profile, id=admin_id)
        community.admins.remove(delete_admin)
        return Response({"message": "Admin removed successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_eligible_admins(request, id):
    community = get_object_or_404(Community, id=id)
    possible_admins = Profile.objects.exclude(id__in=community.admins.all()).exclude(id=community.creator.id)
    admins_serializer = ProfileSerializer(possible_admins, many=True)
    return Response(admins_serializer.data, status=status.HTTP_200_OK)