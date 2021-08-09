from celery import shared_task

from django.core.mail import send_mail as django_send_mail


@shared_task
def contact_us_send_mail(subject, message, from_email, recipient_list):
    django_send_mail(subject, message, from_email, recipient_list)
