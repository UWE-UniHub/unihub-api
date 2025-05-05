from django.urls import path
from comments.views import comment_detail, post_comments
from .views import postsIdGetPatchDelete, postIdImgGetPutDelete, postIdLikesGetPostDelete

urlpatterns = [
    path('/<str:id>', postsIdGetPatchDelete, name='postsIdGetPatchDelete'),
    path('/<str:id>/img', postIdImgGetPutDelete, name='postIdImgGetPutDelete'),
    path('/<str:id>/likes', postIdLikesGetPostDelete, name='postIdLikesGetPostDelete'),
    path('/<str:id>/comments/', post_comments, name='post-comments'),
    path('/<str:id>/comments/<str:comment_id>/', comment_detail, name='comment-detail'),
]