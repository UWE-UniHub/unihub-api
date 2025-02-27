from django.urls import path
from .views import get_profile_by_id, edit_profile, delete_profile

urlpatterns = [
    path('<int:id>/', get_profile_by_id, name="get_profile_by_id"),
    path('<int:id>/edit', edit_profile, name="edit_profile"),
    path('<int:id>/delete', delete_profile, name="delete_profile"),
]