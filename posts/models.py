import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, blank=True)
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.TextField(blank=True, help_text="Comma-separated list of tags")
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(
        'profiles.Profile',
        through='PostLikes',
        related_name='like_posts',
        blank=True
    )

    def clean(self):
        if (self.profile is None and self.community is None) or (self.profile is not None and self.community is not None):
            raise ValidationError("Post must have either a profile or a community author, but not both.")
        
class PostLikes(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post','profile')
        