from django.urls import path
from .views import communitiesGetPost, communitiesGetPatchDelete, community_subscribers, add_delete_comm_subs, community_avatar, add_delete_admin, community_admins, get_eligible_admins
from events.views import eventsCommunityIdGetPost
from posts.views import postsCommunityIdGetPost

urlpatterns = [
    path('', communitiesGetPost, name='communitiesGetPost'),
    path('/<str:id>', communitiesGetPatchDelete, name='communitiesGetPatchDelete'),
    path('/<str:id>/followers', community_subscribers, name='community_subscribers'),
    path('/<str:id>/follow', add_delete_comm_subs, name='add_delete_comm_subs'),
    path('/<str:id>/avatar', community_avatar, name='community_avatar'),
    path('/<str:id>/admins', community_admins, name='community_admins'),
    path('/<str:id>/admins/eligible', get_eligible_admins, name='get_eligible_admins'),
    path('/<str:community_id>/admins/<str:admin_id>', add_delete_admin, name='admin_community'),
    path('/<str:id>/events',eventsCommunityIdGetPost, name='eventsCommunityIdGetPost'),
    path('/<str:id>/posts', postsCommunityIdGetPost, name='postsCommunityIdGetPost')
]