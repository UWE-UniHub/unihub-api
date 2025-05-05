from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from posts.views import visible_posts_queryset
from profiles.models import Profile
from communities.models import Community
from posts.models import Post
from events.models import Event
from profiles.serializers import ProfileSerializer
from communities.serializers import CommunitySerializer
from posts.serializers import PostSerializer
from events.serializers import EventSerializer

@api_view(['GET'])
def search(request):
    q = request.query_params.get('q', '').strip()
    if not q:
        return Response({
            "profiles": [],
            "communities": [],
            "posts": [],
            "events": []
        })

    profiles_qs = Profile.objects.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)    |
        Q(program__icontains=q)      |
        Q(interests__icontains=q)    |
        Q(bio__icontains=q)
    ).distinct()[:5]

    communities_qs = Community.objects.filter(
        Q(name__icontains=q) |
        Q(bio__icontains=q)  |
        Q(tags__icontains=q)
    ).distinct()[:5]

    posts = Post.objects.filter(
        Q(content__icontains=q) |
        Q(tags__icontains=q)
    )
    visible_posts = visible_posts_queryset(request, posts)
    posts_qs = visible_posts[:5]

    events_qs = Event.objects.filter(
        Q(description__icontains=q) |
        Q(location__icontains=q)
    ).distinct()[:5]

    data = {
        "profiles":    ProfileSerializer(profiles_qs,    many=True, context={'request': request}).data,
        "communities": CommunitySerializer(communities_qs, many=True, context={'request': request}).data,
        "posts":       PostSerializer(posts_qs,          many=True, context={'request': request}).data,
        "events":      EventSerializer(events_qs,        many=True, context={'request': request}).data,
    }
    return Response(data, status=status.HTTP_200_OK)
