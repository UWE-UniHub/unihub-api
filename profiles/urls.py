from django.urls import path
from .views import profile_detail, profile_followers, profile_subscriptions, add_delete_prof_subs, profile_avatar
from events.views import get_add_profile_events
from posts.views import get_add_profile_posts

urlpatterns = [
    path('<str:id>', profile_detail, name='profile_detail'),
    path('<str:id>/avatar', profile_avatar, name='profile_avatar'),
    path('<str:id>/followers', profile_followers, name='profile_followers'),
    path('<str:id>/subscriptions', profile_subscriptions, name='profile_subscriptions'),
    path('<str:id>/follow', add_delete_prof_subs, name='add_delete_prof_subs'),
    path('<str:id>/events',get_add_profile_events, name='get_add_profile_events'),
    path('<str:id>/posts', get_add_profile_posts, name='get_add_profile_posts')
]