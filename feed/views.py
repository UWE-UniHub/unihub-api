from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.decorators import api_view
from posts.views import visible_posts_queryset
from unihub.utils import FreemiumPagination

@api_view(['GET'])
def feed(request):
    base = Post.objects.all()
    qs   = visible_posts_queryset(request, base)

    paginator = FreemiumPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = PostSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)