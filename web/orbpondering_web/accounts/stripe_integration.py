"""Stripe integration for subscriptions and billing."""

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import UserProfile


def get_or_create_customer(user) -> str:
    """Get or create a Stripe Customer for this user."""
    profile = user.orb_profile

    if profile.stripe_customer_id:
        return profile.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        metadata={"user_id": str(user.id)},
    )
    profile.stripe_customer_id = customer.id
    profile.save(update_fields=["stripe_customer_id"])
    return customer.id


@require_http_methods(["POST"])
def create_checkout_session(request):
    """Create a Stripe Checkout Session and redirect the user."""
    if not settings.STRIPE_SECRET_KEY:
        return redirect("accounts-pricing")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    price_id = settings.STRIPE_ORB_PRICE_ID
    if not price_id:
        return redirect("accounts-pricing")

    customer_id = get_or_create_customer(request.user)

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=request.build_absolute_uri("/accounts/pricing/?success=1"),
        cancel_url=request.build_absolute_uri("/accounts/pricing/?canceled=1"),
        metadata={"user_id": str(request.user.id)},
    )

    return redirect(session.url, status=303)


@require_http_methods(["GET"])
def billing_portal(request):
    """Redirect user to Stripe Customer Portal to manage their subscription."""
    if not settings.STRIPE_SECRET_KEY:
        return redirect("accounts-pricing")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    customer_id = request.user.orb_profile.stripe_customer_id
    if not customer_id:
        return redirect("accounts-pricing")

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=request.build_absolute_uri("/accounts/pricing/"),
    )

    return redirect(session.url, status=303)


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Handle Stripe webhook events for subscription lifecycle."""
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse("Webhook secret not configured", status=500)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)

    event_type = event.get("type")

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(event["data"]["object"])

    elif event_type == "customer.subscription.updated":
        _handle_subscription_updated(event["data"]["object"])

    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(event["data"]["object"])

    return HttpResponse("OK", status=200)


def _handle_checkout_completed(session):
    """Activate subscription after successful checkout."""
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    if not customer_id:
        return

    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
    except UserProfile.DoesNotExist:
        return

    profile.subscription_status = "active"
    profile.stripe_subscription_id = subscription_id
    profile.save(update_fields=["subscription_status", "stripe_subscription_id"])


def _handle_subscription_updated(subscription):
    """Update subscription status from Stripe."""
    customer_id = subscription.get("customer")
    status = subscription.get("status", "")
    subscription_id = subscription.get("id", "")

    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
    except UserProfile.DoesNotExist:
        return

    status_map = {
        "active": "active",
        "past_due": "past_due",
        "canceled": "free",
        "unpaid": "past_due",
        "incomplete": "free",
        "incomplete_expired": "free",
        "trialing": "active",
        "paused": "free",
    }

    profile.subscription_status = status_map.get(status, "free")
    profile.stripe_subscription_id = subscription_id
    profile.save(update_fields=["subscription_status", "stripe_subscription_id"])


def _handle_subscription_deleted(subscription):
    """Set subscription to free when deleted."""
    customer_id = subscription.get("customer")

    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
    except UserProfile.DoesNotExist:
        return

    profile.subscription_status = "free"
    profile.stripe_subscription_id = ""
    profile.save(update_fields=["subscription_status", "stripe_subscription_id"])
