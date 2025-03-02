from django.urls import path
from .views import profile_detail, profile_followers, profile_subscriptions, add_delete_prof_subs, profile_avatar

urlpatterns = [
    path('<int:id>', profile_detail, name='profile_detail'),

    path('<int:id>/avatar', profile_avatar, name='profile_avatar'),

    path('<int:id>/followers', profile_followers, name='profile_followers'),
    path('<int:id>/subscriptions', profile_subscriptions, name='profile_subscriptions'),
    path('<int:id>/follow', add_delete_prof_subs, name='add_delete_prof_subs'),
]