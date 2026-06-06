"""Account models: profiles, settings, reading history."""

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Subscription and billing metadata for a user."""

    SUBSCRIPTION_CHOICES = [
        ("free", "Free"),
        ("active", "Orb (Active)"),
        ("cancelled", "Orb (Cancelled)"),
        ("past_due", "Orb (Past Due)"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orb_profile"
    )
    subscription_status = models.CharField(
        max_length=20, choices=SUBSCRIPTION_CHOICES, default="free"
    )
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} — {self.subscription_status}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    @property
    def default_profile(self):
        """The user's primary SavedProfile."""
        return self.user.saved_profiles.filter(is_default=True).first()

    @property
    def max_profiles(self):
        return 10 if self.subscription_status == "active" else 1


class SavedProfile(models.Model):
    """A named location profile. Free users get 1, Orb users get up to 10."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_profiles"
    )
    name = models.CharField(max_length=100)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    house_system = models.CharField(max_length=20, default="whole_sign")
    spread = models.CharField(max_length=20, default="daily")
    reversed_cards = models.BooleanField(default=False)
    # Natal chart data
    birth_date = models.DateField(null=True, blank=True)
    birth_time = models.TimeField(null=True, blank=True)
    birth_lat = models.FloatField(default=0.0)
    birth_lon = models.FloatField(default=0.0)
    birth_tz = models.CharField(max_length=100, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    class Meta:
        verbose_name = "Saved Profile"
        verbose_name_plural = "Saved Profiles"
        ordering = ["-is_default", "created_at"]


class ReadingHistory(models.Model):
    """A cached tarot reading for a user on a given date."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="readings"
    )
    date = models.DateField()
    reading_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.date}"

    class Meta:
        verbose_name = "Reading History"
        verbose_name_plural = "Reading History"
        unique_together = [("user", "date")]
        ordering = ["-date"]
