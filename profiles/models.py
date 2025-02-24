from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Profile(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', 'ID must be an 8-digit number.')],
        unique=True
    )
    bio = models.TextField(blank=True)

    username = None
    email = None
    is_staff = models.BooleanField(default=False)

    # student
    program = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)

    # staff
    position = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        through="ProfileSubscription",
        related_name='subscribers',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
   
class ProfileSubscription(models.Model):
    subscriber = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')
