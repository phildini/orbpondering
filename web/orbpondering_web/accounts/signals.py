"""Auto-create UserProfile + default SavedProfile when a new User signs up."""

from django.db.models.signals import post_save


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from .models import SavedProfile, UserProfile

        UserProfile.objects.get_or_create(user=instance)
        SavedProfile.objects.get_or_create(
            user=instance,
            is_default=True,
            defaults={"name": "Default"},
        )


post_save.connect(create_user_profile, sender="auth.User")
