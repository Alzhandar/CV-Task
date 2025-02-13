from cv_project.celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact

@shared_task
def send_notification_email(contact_id):
    try:
        contact = Contact.objects.get(id=contact_id)
        subject = f'Новое контактное сообщение от {contact.name}'
        message = f"""
        Получено новое сообщение:
        
        От: {contact.name}
        Email: {contact.email}
        Сообщение: {contact.message}
        
        Время получения: {contact.created_at.strftime("%d.%m.%Y %H:%M")}
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return str(e)

@shared_task
def clean_old_attachments():
    from datetime import timedelta
    from django.utils import timezone
    
    old_contacts = Contact.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=30),
        attachment__isnull=False
    )
    for contact in old_contacts:
        if contact.attachment:
            contact.attachment.delete()