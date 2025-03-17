from django.urls import path
from .views import postsIdGetPatchDelete

urlpatterns = [
    path('/<str:id>', postsIdGetPatchDelete, name='postsIdGetPatchDelete'),
]