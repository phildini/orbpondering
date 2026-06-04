"""Admin configuration for accounts app."""

from django.contrib import admin

from .models import ReadingHistory, SavedProfile, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "subscription_status", "default_house_system", "default_spread"]
    list_filter = ["subscription_status"]
    search_fields = ["user__email"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(SavedProfile)
class SavedProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "lat", "lon", "created_at"]
    search_fields = ["name", "user__email"]
    list_filter = ["house_system"]


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "created_at"]
    search_fields = ["user__email"]
    date_hierarchy = "date"
