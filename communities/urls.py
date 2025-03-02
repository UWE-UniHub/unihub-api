from django.urls import path
from .views import communitiesGetPost, communitiesGetPatchDelete

urlpatterns = [
    path('', communitiesGetPost, name='communitiesGetPost'),
    path('/<uuid:id>', communitiesGetPatchDelete, name='communitiesGetPatchDelete'),
]