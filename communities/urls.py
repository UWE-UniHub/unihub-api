from django.urls import path
from .views import communitiesGetPost, communitiesGetPatchDelete, community_subscribers, add_delete_comm_subs

urlpatterns = [
    path('', communitiesGetPost, name='communitiesGetPost'),
    path('/<uuid:id>', communitiesGetPatchDelete, name='communitiesGetPatchDelete'),
    path('/<uuid:id>/subscribers', community_subscribers, name='community_subscribers'),
    path('/<uuid:id>/follow', add_delete_comm_subs, name='add_delete_comm_subs')
]