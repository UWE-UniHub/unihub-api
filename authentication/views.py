from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status
from profiles.models import Profile
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from profiles.serializers import ProfileSerializer

@api_view(['GET'])
def auth_check(request):
    token = request.COOKIES.get("token")

    if not token:
            token = request.headers.get("token")
            
    if not token:
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_view(request):
    id = request.data.get("id")
    password = request.data.get("password")

    user = authenticate(id=id, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        update_last_login(None, user)
        response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="token", 
            value=token.key,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response
    
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)