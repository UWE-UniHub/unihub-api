from django.db.models import Q
from posts.models import Post
from communities.models import Community
from profiles.models import Profile
from posts.serializers import PostPostSerializer, PostSerializer
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from profiles.views import get_user_from_request, validate_png
from rest_framework.pagination import LimitOffsetPagination
from unihub.settings import POSTS_IMG_DIR
import os

class FeedPagination(LimitOffsetPagination):
    default_limit = 10  # Количество объектов на странице по умолчанию
    max_limit = 100

@api_view(['GET'])
def feed(request):
    user, error_response = get_user_from_request(request)

    if error_response:
        posts = Post.objects.all()
    else:
        subscribed_profiles = user.subscriptions.all()
        subscribed_communities = Community.objects.filter(subscribers=user)
        posts = Post.objects.filter(Q(profile__in=subscribed_profiles) | Q(community__in=subscribed_communities))
    
    posts = posts.order_by('-created_at')
    paginator = FeedPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)