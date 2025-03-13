from communities.models import Community
from profiles.models import Profile
from .models import Event
from .serializers import EventPostSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from profiles.views import get_user_from_request
from communities.views import check_user_is_admin, check_user_is_community_creator

def check_user_is_event_creator(user, event):
    return event.creator == user

@api_view(['GET'])
def eventsGet(request):
    serializer = EventSerializer(Event.objects.all(),many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PATCH','DELETE'])
def eventsIdGetPatchDelete(request,id):

    event = get_object_or_404(Event,id=id)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response
    
    if check_user_is_event_creator(user, event) or check_user_is_community_creator(user, event.community) or check_user_is_admin(user, event.community):
        
        if request.method == 'PATCH':
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST'])
def eventsProfileIdGetPost(request, id):
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'GET':
        serializer = EventSerializer(Event.objects.filter(creator=profile, community=None), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response

    if str(user.id) != str(id):
        return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    serializer = EventPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['creator_id'] = user.id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def eventsCommunityIdGetPost(request,id):

    community = get_object_or_404(Community, id = id)
    if request.method == 'GET':
        serializer = EventSerializer(Event.objects.filter(community = community), many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response
    
    if check_user_is_community_creator(user, community) or check_user_is_admin(user, community):

        serializer = EventPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['creator_id'] = user.id
            serializer.validated_data['community_id'] = id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
