from django.urls import path
from unihub_app.views import feed

urlpatterns = [
    path('feed', feed, name='feed'),
]