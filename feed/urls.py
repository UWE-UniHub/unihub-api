from django.urls import path
from feed.views import feed

urlpatterns = [
    path('feed', feed, name='feed'),
]