from django.urls import path
from .views import postsIdGetPatchDelete, postIdImgGetPutDelete

urlpatterns = [
    path('/<str:id>', postsIdGetPatchDelete, name='postsIdGetPatchDelete'),
    path('/<str:id>/img', postIdImgGetPutDelete, name='postIdImgGetPutDelete'),
]