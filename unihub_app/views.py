from django.db.models import Q
from posts.models import Post
from communities.models import Community
from posts.serializers import PostSerializer
from rest_framework.decorators import api_view
from profiles.views import get_user_from_request
from unihub.utils import FreemiumPagination

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
    paginator = FreemiumPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)