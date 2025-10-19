from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import JobPosting, Application, AuditLog

# --- JobPosting logs ---
@receiver(post_save, sender=JobPosting)
def log_jobposting_save(sender, instance, created, **kwargs):
    action = "Created job" if created else "Updated job"
    AuditLog.objects.create(user=instance.created_by, action=f"{action}: {instance.title}")

@receiver(post_delete, sender=JobPosting)
def log_jobposting_delete(sender, instance, **kwargs):
    try:
        user = instance.created_by
    except Exception:
        user = None  # if user is already deleted

    AuditLog.objects.create(
        user=user,
        action=f"Deleted job: {instance.title}"
    )




# --- Application logs ---
@receiver(post_save, sender=Application)
def log_application_save(sender, instance, created, **kwargs):
    action = "Submitted application" if created else "Updated application"
    AuditLog.objects.create(user=instance.user, action=f"{action} for job: {instance.job.title}")

@receiver(post_delete, sender=Application)
def log_application_delete(sender, instance, **kwargs):
    AuditLog.objects.create(user=instance.user, action=f"Withdrew application for job: {instance.job.title}")
