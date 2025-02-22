import uuid
from django.db import models

class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    creator = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='created_communities')

    subscribers = models.ManyToManyField(
        'profiles.Profile',
        through='CommunitySubscription',
        related_name='subscribed_communities',
        blank=True
    )

    admins = models.ManyToManyField(
        'profiles.Profile',
        through='CommunityAdmin',
        related_name='admin_communities',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CommunitySubscription(models.Model):
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'community')

class CommunityAdmin(models.Model):
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'community')
