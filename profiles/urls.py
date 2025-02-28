from django.urls import path
from .views import profile_detail

urlpatterns = [
    path('<int:id>/', profile_detail, name='profile_detail'),
]