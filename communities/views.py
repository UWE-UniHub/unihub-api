from .models import Community
from .serializers import CommunitySerializer, CommunityPostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

def get_user_from_token(request):
    token = request.COOKIES.get("token")

    if not token:
        return None, Response({"error": "No token provided"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = Token.objects.get(key=token).user
        return user, None
    except Token.DoesNotExist:
        return None, Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','POST'])
def communitiesGetPost(request):

    if request.method == 'GET':
        serializer = CommunitySerializer(Community.objects.all(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        #request.data['creator_id'] = user.id
        serializer = CommunityPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['creator_id'] = user.id
            serializer.save()
            community = get_object_or_404(Community,id=serializer.data['id'])
            community.admins.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@api_view(['PATCH','DELETE'])