from django.contrib import admin
from .models import (
    User, Profile, JobPosting, Application,
    Bookmark, AuditLog, RecommendationAudit
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "last_profile_update")
    search_fields = ("user__username", "skills", "education")

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "created_at")
    search_fields = ("title", "company", "description")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status", "applied_at")
    search_fields = ("user__username", "job__title")

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "saved_at")
    search_fields = ("user__username", "job__title")

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "created_at")
    search_fields = ("action", "user__username")

@admin.register(RecommendationAudit)
class RecommendationAuditAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "match_score", "created_at")
    search_fields = ("user__username", "job__title", "explanation")
