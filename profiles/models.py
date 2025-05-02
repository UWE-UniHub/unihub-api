from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from profiles.managers import CustomUserManager

class Profile(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', 'ID must be an 8-digit number.')],
        unique=True
    )
    bio = models.TextField(blank=True)
    username = None
    email = models.EmailField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    interests = models.TextField(blank=True, help_text="Comma-separated list of interests")

    # student
    program = models.CharField(max_length=255, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
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

    objects = CustomUserManager() 

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
   
class ProfileSubscription(models.Model):
    subscriber = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')
