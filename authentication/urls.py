from django.urls import path
from .views import get_departments, get_schools, login_view, signup_view, auth_check, logout_view

urlpatterns = [
    path('auth/login', login_view, name='login'),
    path('auth/signup', signup_view, name='signup'),
    path('auth', auth_check, name='auth_check'),
    path('auth/logout', logout_view, name='logout'),

    path('schools', get_schools, name='get_schools'),
    path('departments', get_departments, name='get_departments'),
]
