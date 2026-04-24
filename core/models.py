from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

# ---------------------------
# ✅ Custom User model
# ---------------------------
class User(AbstractUser):
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ---------------------------
# ✅ Profile linked to custom User model
# ---------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    # ✅ Professional Details
    skills = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=50, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    certificates = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    extracurriculars = models.TextField(blank=True, null=True)
    hackathons = models.TextField(blank=True, null=True)

    # ✅ For future AI recommendation
    skill_vector = models.JSONField(blank=True, null=True)
    last_profile_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ---------------------------
# ✅ Job Posting model
# ---------------------------
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
        ("Remote", "Remote"),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ("Entry", "Entry Level"),
        ("Mid", "Mid Level"),
        ("Senior", "Senior Level"),
        ("Manager", "Manager"),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ("On-site", "On-site"),
        ("Hybrid", "Hybrid"),
        ("Remote", "Remote"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default="Full-time")
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, default="Entry")
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, default="On-site")
    remote_option = models.BooleanField(default=False)
    skills_required = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="posted_jobs")
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ For AI skill matching
    skill_requirements = models.TextField(blank=True, null=True)
    skill_vector = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


# ---------------------------
# ✅ Application model
# ---------------------------
class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    ]

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ("job", "user")

    def __str__(self):
        return f"{self.user.username} → {self.job.title} ({self.status})"


# ---------------------------
# ✅ Bookmark model
# ---------------------------
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="bookmarked_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.job.title}"


# ---------------------------
# ✅ Audit Log
# ---------------------------
class AuditLog(models.Model):
    action = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} - {self.action}"


# ---------------------------
# ✅ Recommendation Audit
# ---------------------------
class RecommendationAudit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendation_audits")
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    match_score = models.FloatField()
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RecAudit: {self.user.username} → {self.job.title} ({self.match_score:.1f}%)"


# ---------------------------
# ✅ Password Reset Code (5-digit system)
# ---------------------------
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - {self.code}"


# ---------------------------
# ✅ Signal: Create Profile automatically
# ---------------------------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)


# ---------------------------
# ✅ Notifications
# ---------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"
