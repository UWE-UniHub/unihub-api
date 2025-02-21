import uuid
from django.db import models

class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    creator = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='created_communities')
    subscribers = models.ManyToManyField('profiles.Profile', related_name='subscribed_communities', blank=True)
    admins = models.ManyToManyField('profiles.Profile', related_name='admin_communities', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)