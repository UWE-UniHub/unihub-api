from django.urls import path
from .views import add_delete_event_sub, event_subscribers, eventsGet, eventsIdGetPatchDelete, eventsNotifSend

urlpatterns = [
    path('', eventsGet, name='eventsGet'),
    path('/<str:id>',eventsIdGetPatchDelete, name='eventsIdGetPatchDelete'),
    path('/<str:id>/subscribers', event_subscribers, name='event_subscribers'),
    path('/<str:id>/subscribe', add_delete_event_sub, name='add_delete_event_sub'),
    path('/notify/all', eventsNotifSend, name='notify'),
]
