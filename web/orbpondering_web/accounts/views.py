"""Account views: dashboard, settings, profiles, pricing."""

from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orbpondering.constants import HouseSystem
from orbpondering.draw import tarot_draw_for_date

from .models import ReadingHistory, SavedProfile


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
    profile = request.user.orb_profile.default_profile
    if profile is None:
        return redirect("accounts-settings")

    # Past 7 days — from DB
    past_start = today - timedelta(days=7)
    past_readings = {
        rh.date: rh.reading_data
        for rh in ReadingHistory.objects.filter(user=request.user, date__gte=past_start)
    }

    # Future 8 days (today + next 7)
    future_dates = [today + timedelta(days=i) for i in range(8)]

    days = []
    for d in future_dates:
        reading_data = past_readings.get(d)
        if reading_data:
            summary = _reading_to_card_summary(reading_data)
            summary["from_db"] = True
        else:
            try:
                house = HouseSystem(profile.house_system)
                reading = tarot_draw_for_date(
                    d=d,
                    lat=profile.lat,
                    lon=profile.lon,
                    house_system=house,
                    spread_name=profile.spread,
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
        {"days": days},
    )


@login_required
def settings_view(request):
    """View and update the user's default SavedProfile."""
    profile = request.user.orb_profile.default_profile
    if profile is None:
        profile = SavedProfile.objects.create(
            user=request.user, name="Default", is_default=True
        )

    if request.method == "POST":
        try:
            profile.lat = float(request.POST.get("lat", "0.0"))
        except ValueError:
            pass
        try:
            profile.lon = float(request.POST.get("lon", "0.0"))
        except ValueError:
            pass
        profile.house_system = request.POST.get("house_system", "whole_sign")
        profile.spread = request.POST.get("spread", "daily")
        profile.reversed_cards = request.POST.get("reversed") == "on"
        # Natal fields
        bd = request.POST.get("birth_date", "").strip()
        if bd:
            from datetime import datetime
            try:
                profile.birth_date = datetime.strptime(bd, "%Y-%m-%d").date()
            except ValueError:
                pass
        else:
            profile.birth_date = None
        bt = request.POST.get("birth_time", "").strip()
        if bt:
            from datetime import datetime
            try:
                profile.birth_time = datetime.strptime(bt, "%H:%M").time()
            except ValueError:
                pass
        else:
            profile.birth_time = None
        try:
            profile.birth_lat = float(request.POST.get("birth_lat", "0.0"))
        except ValueError:
            pass
        try:
            profile.birth_lon = float(request.POST.get("birth_lon", "0.0"))
        except ValueError:
            pass
        profile.birth_tz = request.POST.get("birth_tz", "")
        profile.save()
        return redirect("accounts-settings")

    return render(
        request,
        "accounts/settings.html",
        {"profile": profile, "max_profiles": request.user.orb_profile.max_profiles},
    )


@login_required
def profiles_view(request):
    """List and manage saved profiles (Orb for additional ones)."""
    orb_profile = request.user.orb_profile
    is_orb = orb_profile.subscription_status == "active"
    max_profiles = orb_profile.max_profiles

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            name = request.POST.get("name", "").strip()
            if name and request.user.saved_profiles.count() < max_profiles:
                try:
                    lat = float(request.POST.get("lat", "0.0"))
                except ValueError:
                    lat = 0.0
                try:
                    lon = float(request.POST.get("lon", "0.0"))
                except ValueError:
                    lon = 0.0
                bd = request.POST.get("birth_date", "").strip()
                birth_date = None
                if bd:
                    from datetime import datetime
                    try:
                        birth_date = datetime.strptime(bd, "%Y-%m-%d").date()
                    except ValueError:
                        pass
                bt = request.POST.get("birth_time", "").strip()
                birth_time = None
                if bt:
                    from datetime import datetime
                    try:
                        birth_time = datetime.strptime(bt, "%H:%M").time()
                    except ValueError:
                        pass
                try:
                    birth_lat = float(request.POST.get("birth_lat", "0.0"))
                except ValueError:
                    birth_lat = 0.0
                try:
                    birth_lon = float(request.POST.get("birth_lon", "0.0"))
                except ValueError:
                    birth_lon = 0.0
                SavedProfile.objects.create(
                    user=request.user,
                    name=name,
                    lat=lat,
                    lon=lon,
                    house_system=request.POST.get("house_system", "whole_sign"),
                    spread=request.POST.get("spread", "daily"),
                    reversed_cards=request.POST.get("reversed") == "on",
                    birth_date=birth_date,
                    birth_time=birth_time,
                    birth_lat=birth_lat,
                    birth_lon=birth_lon,
                    birth_tz=request.POST.get("birth_tz", ""),
                )
        elif action == "delete":
            SavedProfile.objects.filter(
                id=request.POST.get("id"), user=request.user, is_default=False
            ).delete()
        elif action == "set_default":
            SavedProfile.objects.filter(user=request.user).update(is_default=False)
            SavedProfile.objects.filter(
                id=request.POST.get("id"), user=request.user
            ).update(is_default=True)
        return redirect("accounts-profiles")

    saved = request.user.saved_profiles.all()
    count = saved.count()
    return render(
        request,
        "accounts/profiles.html",
        {
            "profiles": saved,
            "profile_count": count,
            "max_profiles": max_profiles,
            "is_orb": is_orb,
        },
    )


@login_required
def subscribe_view(request):
    """Redirect to Stripe Checkout or billing portal."""
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "subscribe":
            if settings.STRIPE_SECRET_KEY:
                from .stripe_integration import create_checkout_session
                return create_checkout_session(request)
            # Fallback to mock for development
            profile = request.user.orb_profile
            profile.subscription_status = "active"
            profile.save()
            return redirect("accounts-pricing")
        elif action == "unsubscribe":
            if settings.STRIPE_SECRET_KEY and request.user.orb_profile.stripe_customer_id:
                from .stripe_integration import billing_portal
                return billing_portal(request)
            # Fallback to mock for development
            profile = request.user.orb_profile
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
    has_stripe = bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_ORB_PRICE_ID)
    return render(
        request,
        "accounts/pricing.html",
        {
            "is_orb": is_orb,
            "price_dollars": price / 100,
            "must_upgrade": request.GET.get("upgrade") == "1",
            "has_stripe": has_stripe,
        },
    )
