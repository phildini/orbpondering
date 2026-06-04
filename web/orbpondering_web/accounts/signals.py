"""Auto-create UserProfile when a new User is created."""

from django.db.models.signals import post_save


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from .models import UserProfile

        UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender="auth.User")
