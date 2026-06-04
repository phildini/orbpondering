"""Account views: dashboard, settings, profiles, pricing."""

from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orbpondering.constants import HouseSystem
from orbpondering.draw import tarot_draw_for_date

from .models import ReadingHistory, SavedProfile


def _save_reading_for_user(user, reading):
    """Store a reading in the user's history."""
    from orbpondering_web.frontend.views import _build_reading_context

    context = _build_reading_context(reading)
    data = context.get("reading", {})
    ReadingHistory.objects.update_or_create(
        user=user,
        date=reading.date,
        defaults={"reading_data": data},
    )


def _reading_to_card_summary(rd):
    """Extract a card summary from a reading dict for template display."""
    positions = rd.get("positions", [])
    cards = []
    for p in positions:
        card = p.get("card", {})
        cards.append(
            {
                "name": card.get("name", "?"),
                "arcana": card.get("arcana", ""),
                "element": card.get("element", ""),
                "upright": card.get("upright", True),
                "label": p.get("label", ""),
            }
        )
    return {
        "spread": rd.get("spread", {}).get("name", "Reading"),
        "seed": rd.get("seed", ""),
        "cards": cards,
    }


@login_required
def dashboard(request):
    """Show past 7 and next 7 days of readings."""
    today = date.today()
    profile = request.user.orb_profile

    # Past 7 days — from DB
    past_start = today - timedelta(days=7)
    past_readings = {
        rh.date: rh.reading_data
        for rh in ReadingHistory.objects.filter(user=request.user, date__gte=past_start)
    }

    # Future 7 days — pre-compute from saved prefs
    future_dates = [today + timedelta(days=i) for i in range(8)]  # today + next 7

    days = []
    for d in future_dates:
        reading_data = past_readings.get(d)
        if reading_data:
            summary = _reading_to_card_summary(reading_data)
            summary["from_db"] = True
        else:
            # Pre-compute
            try:
                house = HouseSystem(profile.default_house_system)
                reading = tarot_draw_for_date(
                    d=d,
                    lat=profile.default_lat,
                    lon=profile.default_lon,
                    house_system=house,
                    spread_name=profile.default_spread,
                    reversed_cards=profile.reversed_cards,
                )
                from orbpondering_web.frontend.views import _build_reading_context
                ctx = _build_reading_context(reading)
                summary = _reading_to_card_summary(ctx.get("reading", {}))
                summary["from_db"] = False
            except Exception:
                summary = None

        days.append(
            {
                "date": d,
                "is_today": d == today,
                "is_future": d > today,
                "reading": summary,
            }
        )

    return render(
        request,
        "accounts/dashboard.html",
        {"days": days, "profile": profile},
    )


@login_required
def settings_view(request):
    """View and update user preferences."""
    profile = request.user.orb_profile

    if request.method == "POST":
        try:
            profile.default_lat = float(request.POST.get("lat", "0.0"))
        except ValueError:
            pass
        try:
            profile.default_lon = float(request.POST.get("lon", "0.0"))
        except ValueError:
            pass
        profile.default_house_system = request.POST.get("house_system", "whole_sign")
        profile.default_spread = request.POST.get("spread", "daily")
        profile.reversed_cards = request.POST.get("reversed") == "on"
        profile.save()
        return redirect("accounts-settings")

    return render(
        request,
        "accounts/settings.html",
        {"profile": profile},
    )


@login_required
def profiles_view(request):
    """List and manage saved profiles (Orb subscribers only)."""
    profile = request.user.orb_profile
    is_orb = profile.subscription_status == "active"

    if not is_orb:
        return render(request, "accounts/pricing.html", {"must_upgrade": True})

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            name = request.POST.get("name", "").strip()
            if name and request.user.saved_profiles.count() < 10:
                try:
                    lat = float(request.POST.get("lat", "0.0"))
                except ValueError:
                    lat = 0.0
                try:
                    lon = float(request.POST.get("lon", "0.0"))
                except ValueError:
                    lon = 0.0
                SavedProfile.objects.create(
                    user=request.user,
                    name=name,
                    lat=lat,
                    lon=lon,
                    house_system=request.POST.get("house_system", "whole_sign"),
                    spread=request.POST.get("spread", "daily"),
                    reversed_cards=request.POST.get("reversed") == "on",
                )
        elif action == "delete":
            SavedProfile.objects.filter(
                id=request.POST.get("id"), user=request.user
            ).delete()
        return redirect("accounts-profiles")

    saved = request.user.saved_profiles.all()
    return render(
        request,
        "accounts/profiles.html",
        {"profiles": saved, "profile_count": saved.count(), "max_profiles": 10},
    )


@login_required
def subscribe_view(request):
    """Mock subscription toggle for development."""
    profile = request.user.orb_profile
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "subscribe":
            profile.subscription_status = "active"
            profile.save()
        elif action == "unsubscribe":
            profile.subscription_status = "free"
            profile.save()
        return redirect("accounts-pricing")
    return redirect("accounts-pricing")


def pricing_view(request):
    """Show pricing plans."""
    is_orb = False
    if request.user.is_authenticated:
        is_orb = request.user.orb_profile.subscription_status == "active"
    price = getattr(settings, "ORB_PRICE_CENTS", 499)
    return render(
        request,
        "accounts/pricing.html",
        {
            "is_orb": is_orb,
            "price_dollars": price / 100,
            "must_upgrade": request.GET.get("upgrade") == "1",
        },
    )
