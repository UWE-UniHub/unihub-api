from .models import Post
from communities.models import Community
from profiles.models import Profile
from .serializers import PostPostSerializer, PostSerializer
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from profiles.views import get_user_from_request, validate_png
from communities.views import check_user_is_admin, check_user_is_community_creator
from unihub.settings import POSTS_IMG_DIR
import os

def check_user_can_pD_posts(user,post):
    return post.profile == user if post.profile else check_user_is_admin(user,post.community) or check_user_is_community_creator(user,post.community)

@api_view(['GET','PATCH','DELETE'])
def postsIdGetPatchDelete(request,id):

    post = get_object_or_404(Post,id=id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response
    
    if check_user_can_pD_posts(user, post):
        
        if request.method == 'PATCH':
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST'])
def postsProfileIdGetPost(request, id):
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'GET':
        serializer = PostSerializer(Post.objects.filter(profile=profile), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response

    if str(user.id) != str(id):
        return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    serializer = PostPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['profile_id'] = user.id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def postsCommunityIdGetPost(request,id):

    community = get_object_or_404(Community, id = id)
    if request.method == 'GET':
        serializer = PostSerializer(Post.objects.filter(community = community), many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response
    
    if check_user_is_community_creator(user, community) or check_user_is_admin(user, community):

        serializer = PostPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['community_id'] = id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PUT', 'DELETE'])
def postIdImgGetPutDelete(request, id):
    post = get_object_or_404(Post, id=id)
    img_path = os.path.join(POSTS_IMG_DIR, f"{id}.png")

    if request.method == 'GET':
        if os.path.exists(img_path):
            return FileResponse(open(img_path, 'rb'), content_type='image/png')
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user, error_response = get_user_from_request(request)
    if error_response:
        return error_response
    
    if check_user_can_pD_posts(user,post):    
        if request.method == 'PUT':
            if not request.body:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
            
            is_png, error_message = validate_png(request.body)
            if not is_png:
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                with open(img_path, 'wb') as f:
                    f.write(request.body)
                return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to save image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        if os.path.exists(img_path):
            os.remove(img_path)
            return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"error": "You are not allowed to perform this action."}, status=status.HTTP_403_FORBIDDEN)
