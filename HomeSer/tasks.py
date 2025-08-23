# HomeSer/tasks.py
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def debug_task():
    """Simple debug task to test Celery configuration"""
    return "Hello from Celery!"


@shared_task
def send_email_task(subject, message, recipient_list):
    """Task to send emails asynchronously"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return f"Email sent successfully to {', '.join(recipient_list)}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
