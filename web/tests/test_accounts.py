"""Tests for the accounts app: models, views, and signal behavior."""

import pytest


# ---- Model tests ----

class TestUserProfileSignal:
    def test_user_created_signal_creates_profile(self, db):
        """Creating a User should auto-create UserProfile + default SavedProfile."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        from orbpondering_web.accounts.models import SavedProfile, UserProfile

        assert UserProfile.objects.filter(user=user).exists()
        assert SavedProfile.objects.filter(user=user, is_default=True).exists()

    def test_default_profile_has_default_values(self, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        profile = user.orb_profile.default_profile
        assert profile.name == "Default"
        assert profile.lat == 0.0
        assert profile.lon == 0.0
        assert profile.house_system == "whole_sign"
        assert profile.spread == "daily"
        assert profile.reversed_cards is False


class TestUserProfile:
    def test_str(self, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import UserProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        profile = UserProfile.objects.get(user=user)
        assert "test@example.com — free" in str(profile)

    def test_max_profiles_free(self, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        assert user.orb_profile.max_profiles == 1

    def test_max_profiles_orb(self, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        user.orb_profile.subscription_status = "active"
        user.orb_profile.save()
        assert user.orb_profile.max_profiles == 10

    def test_default_profile_property(self, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        dp = user.orb_profile.default_profile
        assert dp.is_default is True
        assert dp.user == user


class TestSavedProfile:
    def test_create_additional_profile(self, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import SavedProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        p2 = SavedProfile.objects.create(
            user=user, name="Home", lat=40.0, lon=-74.0
        )
        assert p2.name == "Home"
        assert p2.lat == 40.0
        assert not p2.is_default
        assert user.saved_profiles.count() == 2


class TestReadingHistory:
    def test_create_reading_history(self, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import ReadingHistory

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        rh = ReadingHistory.objects.create(
            user=user,
            date="2026-06-01",
            reading_data={"seed": 123, "spread": {"name": "Test"}},
        )
        assert rh.reading_data["seed"] == 123
        assert str(rh) == f"test@example.com — 2026-06-01"

    def test_unique_per_user_per_date(self, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import ReadingHistory
        from django.db import IntegrityError

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        ReadingHistory.objects.create(user=user, date="2026-06-01", reading_data={})
        with pytest.raises(IntegrityError):
            ReadingHistory.objects.create(
                user=user, date="2026-06-01", reading_data={}
            )


# ---- View tests ----

class TestPricingView:
    def test_pricing_page_public(self, client, db):
        resp = client.get("/accounts/pricing/")
        assert resp.status_code == 200
        assert "Orb" in resp.content.decode()
        assert "Free" in resp.content.decode()

    def test_pricing_shows_subscribe_button_when_logged_in_free(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        resp = client.get("/accounts/pricing/")
        html = resp.content.decode()
        assert "Subscribe" in html
        assert "Cancel Subscription" not in html

    def test_pricing_shows_cancel_when_subscribed(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        user.orb_profile.subscription_status = "active"
        user.orb_profile.save()
        client.force_login(user)
        resp = client.get("/accounts/pricing/")
        html = resp.content.decode()
        assert "Cancel Subscription" in html


class TestDashboardView:
    def test_requires_login(self, client, db):
        resp = client.get("/accounts/dashboard/")
        assert resp.status_code == 302

    def test_loads_for_authenticated_user(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        resp = client.get("/accounts/dashboard/")
        assert resp.status_code == 200
        assert "Your Readings" in resp.content.decode()


class TestSettingsView:
    def test_requires_login(self, client, db):
        resp = client.get("/accounts/settings/")
        assert resp.status_code == 302

    def test_loads_with_default_values(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        resp = client.get("/accounts/settings/")
        html = resp.content.decode()
        assert "0.0" in html  # default lat/lon
        assert "whole_sign" in html

    def test_post_updates_profile(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        client.post(
            "/accounts/settings/",
            {
                "lat": "40.71",
                "lon": "-74.00",
                "house_system": "equal",
                "spread": "three_card",
            },
        )
        profile = user.orb_profile.default_profile
        assert profile.lat == 40.71
        assert profile.lon == -74.00
        assert profile.house_system == "equal"
        assert profile.spread == "three_card"


class TestProfilesView:
    def test_requires_login(self, client, db):
        resp = client.get("/accounts/profiles/")
        assert resp.status_code == 302

    def test_can_create_profile(self, client, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import SavedProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        user.orb_profile.subscription_status = "active"
        user.orb_profile.save()
        client.force_login(user)
        client.post(
            "/accounts/profiles/",
            {"action": "create", "name": "Home", "lat": "34.05", "lon": "-118.24"},
        )
        assert SavedProfile.objects.filter(user=user, name="Home").exists()

    def test_free_user_cannot_create_second_profile(self, client, db):
        """Free users have max_profiles=1, so creating a second should fail."""
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import SavedProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        # Try to create a second profile
        client.post(
            "/accounts/profiles/",
            {"action": "create", "name": "Home", "lat": "34.05", "lon": "-118.24"},
        )
        assert SavedProfile.objects.filter(user=user).count() == 1  # only default

    def test_orb_user_can_create_multiple_profiles(self, client, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import SavedProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        user.orb_profile.subscription_status = "active"
        user.orb_profile.save()
        client.force_login(user)
        client.post(
            "/accounts/profiles/",
            {"action": "create", "name": "Home", "lat": "34.05", "lon": "-118.24"},
        )
        assert SavedProfile.objects.filter(user=user).count() == 2  # default + Home

    def test_delete_non_default_profile(self, client, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import SavedProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        user.orb_profile.subscription_status = "active"
        user.orb_profile.save()
        client.force_login(user)
        client.post(
            "/accounts/profiles/",
            {"action": "create", "name": "Work", "lat": "40.0", "lon": "-74.0"},
        )
        work = SavedProfile.objects.get(user=user, name="Work")
        client.post(
            "/accounts/profiles/", {"action": "delete", "id": str(work.id)}
        )
        assert not SavedProfile.objects.filter(id=work.id).exists()
        assert SavedProfile.objects.filter(user=user).count() == 1  # default remains

    def test_cannot_delete_default_profile(self, client, db):
        from django.contrib.auth import get_user_model
        from orbpondering_web.accounts.models import SavedProfile

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        default = SavedProfile.objects.get(user=user, is_default=True)
        client.post(
            "/accounts/profiles/", {"action": "delete", "id": str(default.id)}
        )
        # Default should still exist
        assert SavedProfile.objects.filter(id=default.id).exists()


class TestSubscribeView:
    def test_subscribe_mock(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        client.force_login(user)
        client.post("/accounts/subscribe/", {"action": "subscribe"})
        user.orb_profile.refresh_from_db()
        assert user.orb_profile.subscription_status == "active"

    def test_unsubscribe_mock(self, client, db):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com")
        user.orb_profile.subscription_status = "active"
        user.orb_profile.save()
        client.force_login(user)
        client.post("/accounts/subscribe/", {"action": "unsubscribe"})
        user.orb_profile.refresh_from_db()
        assert user.orb_profile.subscription_status == "free"
