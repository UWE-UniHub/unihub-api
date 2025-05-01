import uuid
from django.db import models

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    creator = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='created_events')
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, null=True, blank=True, related_name='events')
    required_materials = models.TextField(blank=True, null=True)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    subscribers = models.ManyToManyField(
        'profiles.Profile',
        through='EventSubscription',
        related_name='subscribed_events',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EventSubscription(models.Model):
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'event')