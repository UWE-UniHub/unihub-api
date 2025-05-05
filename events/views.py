from communities.models import Community
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .models import Event
from .serializers import EventPostSerializer, EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from profiles.views import get_user_from_request
from communities.views import check_user_is_admin, check_user_is_community_creator
from datetime import datetime, timedelta
from unihub.utils import send_email

def check_user_is_event_creator(user, event):
    return event.creator == user

def clean_up_events():
    Event.objects.filter(date__lt = (datetime.now() - timedelta(days=7)) ).delete()

@api_view(['GET'])
def get_events(request):
    clean_up_events()
    serializer = EventSerializer(Event.objects.all(),many = True, context={'request': request, 'user': request.user})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PATCH','DELETE'])
def get_edit_delete_events(request,id):
    event = get_object_or_404(Event,id=id)
    if request.method == 'GET':
        serializer = EventSerializer(event, context={'request': request, 'user': request.user})
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
def get_add_profile_events(request, id):
    profile = get_object_or_404(Profile, id=id)
    if request.method == 'GET':
        clean_up_events()
        serializer = EventSerializer(Event.objects.filter(creator=profile, community=None), many=True, context={'request': request, 'user': request.user})
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
def get_add_community_events(request,id):
    community = get_object_or_404(Community, id = id)
    if request.method == 'GET':
        clean_up_events()
        serializer = EventSerializer(Event.objects.filter(community = community), many = True, context={'request': request, 'user': request.user})
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

@api_view(['GET'])
def event_subscribers(request, id):
    event = get_object_or_404(Event, id=id)
    subs = event.subscribers.all()
    serializer = ProfileSerializer(subs, many=True)
    return Response(serializer.data)

@api_view(['POST','DELETE'])
def add_delete_event_sub(request, id):
    event = get_object_or_404(Event, id=id)
    user, err = get_user_from_request(request)
    if err: return err
    
    if request.method == 'POST':
        event.subscribers.add(user)
        if event.community:
            host = event.community
        else:
            host = event.creator.first_name
        msg = f"You have subscribed to {host}'s event on {event.date.date()}. {event.description}. We will remind you 1 hour before the event starts!"
        reciever = get_object_or_404(Profile,id=user.id)
        send_email(reciever=reciever,subject="You have subscribed to an event", text=msg)
        return Response({"message":"Subscribed to event"}, status=status.HTTP_200_OK)
    else:
        event.subscribers.remove(user)
        return Response({"message":"Unsubscribed from event"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def events_send_notif(request):
    events = Event.objects.filter(date__lte = (datetime.now() + timedelta(hours=1)))
    for event in events:
        for sub in event.subscribers.all():
            mats = f"And don't forget to bring: {event.required_materials}. " if event.required_materials else ""
            send_email(reciever=sub,subject="Event notification",text=f"{event.description} is starting soon! Come to {event.location} at {event.date.time().strftime('%H:%M')}. {mats}")
    return Response("OK", status=status.HTTP_200_OK)
