from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(AbstractUser):
    id = models.PositiveIntegerField(
        primary_key=True,
        validators=[MinValueValidator(10000000), MaxValueValidator(99999999)],
        unique=True
    )
    bio = models.TextField(blank=True)
    username = None
    is_staff = models.BooleanField(default=False)
    program = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
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

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def followers(self):
        return self.followers.all()

class ProfileSubscription(models.Model):
    subscriber = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')
