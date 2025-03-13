from django.urls import path
from .views import eventsGet, eventsIdGetPatchDelete, eventsProfileIdGetPost

urlpatterns = [
    path('', eventsGet, name='eventsGet'),
    path('/<str:id>',eventsIdGetPatchDelete, name='eventsIdGetPatchDelete'),
    # path('../profiles/<str:id>/events',eventsProfileIdGetPost, name='eventsProfileIdGetPost'),
]