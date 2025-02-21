from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Profile(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', 'ID must be an 8-digit number.')], # Валидация
        unique=True
    )
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    program = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    subscriptions = models.ManyToManyField('self', symmetrical=False, related_name='subscribers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)