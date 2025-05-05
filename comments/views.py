from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from unihub.utils import FreemiumPagination, get_user_from_request
from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer, CommentCreateSerializer
from posts.views import check_user_can_pD_posts, visible_posts_queryset

@api_view(['GET', 'POST'])
def post_comments(request, id):
    base = Post.objects.filter(id=id)
    qs = visible_posts_queryset(request, base)
    post = get_object_or_404(qs, id=id)

    if request.method == 'GET':
        qs = post.comments.all().order_by('created_at')
        page = FreemiumPagination().paginate_queryset(qs, request)
        serializer = CommentSerializer(page, many=True, context={'request': request})
        return FreemiumPagination().get_paginated_response(serializer.data)

    user, err = get_user_from_request(request)
    if err:
        return err

    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        comment = serializer.save(post=post, author=user)
        read = CommentSerializer(comment, context={'request': request})
        return Response(read.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def comment_detail(request, comment_id):
    base = Post.objects.filter(id=id)
    qs = visible_posts_queryset(request, base)
    _ = get_object_or_404(qs, id=id)

    comment = get_object_or_404(Comment, id=comment_id, post__id=id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    user, err = get_user_from_request(request)
    if err:
        return err

    if not (
        comment.author == user
        or check_user_can_pD_posts(user, comment.post)
    ):
        return Response(
            {"error": "You are not allowed to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PATCH':
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CommentSerializer(comment, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
