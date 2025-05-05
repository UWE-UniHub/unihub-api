from django.urls import path
from .views import add_delete_event_sub, event_subscribers, get_events, get_edit_delete_events, events_send_notif

urlpatterns = [
    path('', get_events, name='get_events'),
    path('/<str:id>',get_edit_delete_events, name='get_edit_delete_events'),
    path('/<str:id>/subscribers', event_subscribers, name='event_subscribers'),
    path('/<str:id>/subscribe', add_delete_event_sub, name='add_delete_event_sub'),
    path('/notify/all', events_send_notif, name='notify'),
]
