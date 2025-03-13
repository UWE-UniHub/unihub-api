from django.urls import path
from .views import communitiesGetPost, communitiesGetPatchDelete, community_subscribers, add_delete_comm_subs, community_avatar, add_delete_admin, community_admins, community_posts

urlpatterns = [
    path('', communitiesGetPost, name='communitiesGetPost'),
    path('/<str:id>', communitiesGetPatchDelete, name='communitiesGetPatchDelete'),
    path('/<str:id>/followers', community_subscribers, name='community_subscribers'),
    path('/<str:id>/follow', add_delete_comm_subs, name='add_delete_comm_subs'),
    path('/<str:id>/avatar', community_avatar, name='community_avatar'),
    path('/<str:id>/admins', community_admins, name='community_admins'),
    path('/<str:community_id>/admins/<str:admin_id>', add_delete_admin, name='admin_community'),
    path('/<str:id>/posts', community_posts, name='community_posts'),
]