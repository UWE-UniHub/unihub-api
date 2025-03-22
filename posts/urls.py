from django.urls import path
from .views import postsIdGetPatchDelete, postIdImgGetPutDelete, postIdLikesGetPostDelete

urlpatterns = [
    path('/<str:id>', postsIdGetPatchDelete, name='postsIdGetPatchDelete'),
    path('/<str:id>/img', postIdImgGetPutDelete, name='postIdImgGetPutDelete'),
    path('/<str:id>/likes', postIdLikesGetPostDelete, name='postIdLikesGetPostDelete'),
]