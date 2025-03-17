from django.urls import path
from .views import eventsGet, eventsIdGetPatchDelete

urlpatterns = [
    path('', eventsGet, name='eventsGet'),
    path('/<str:id>',eventsIdGetPatchDelete, name='eventsIdGetPatchDelete'),
]