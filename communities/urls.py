from django.urls import path
from .views import get_add_communities, get_edit_delete_communities, community_subscribers, add_delete_comm_subs, community_avatar, add_delete_admin, community_admins, get_eligible_admins
from events.views import get_add_community_events
from posts.views import get_add_community_posts

urlpatterns = [
    path('', get_add_communities, name='get_add_communities'),
    path('/<str:id>', get_edit_delete_communities, name='get_edit_delete_communities'),
    path('/<str:id>/followers', community_subscribers, name='community_subscribers'),
    path('/<str:id>/follow', add_delete_comm_subs, name='add_delete_comm_subs'),
    path('/<str:id>/avatar', community_avatar, name='community_avatar'),
    path('/<str:id>/admins', community_admins, name='community_admins'),
    path('/<str:id>/admins/eligible', get_eligible_admins, name='get_eligible_admins'),
    path('/<str:community_id>/admins/<str:admin_id>', add_delete_admin, name='admin_community'),
    path('/<str:id>/events',get_add_community_events, name='get_add_community_events'),
    path('/<str:id>/posts', get_add_community_posts, name='postsCommunityIdGetPost')
]