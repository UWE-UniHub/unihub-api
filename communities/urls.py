from django.urls import path
from .views import communitiesGetPost

urlpatterns = [
    path('', communitiesGetPost, name='communitiesGetPost'),
]