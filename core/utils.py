from django.core.mail import send_mail
from .models import Notification

def notify_user(user, message, email_subject=None):
    # In-app notification
    Notification.objects.create(user=user, message=message)

    # Email notification
    if email_subject:
        send_mail(
            subject=email_subject,
            message=message,
            from_email="noreply@accessjobs.com",
            recipient_list=[user.email],
            fail_silently=True,
        )
