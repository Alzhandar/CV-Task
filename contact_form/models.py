from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

class Contact(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    attachment = models.ImageField('Прикрепленное изображение', 
                                 upload_to='contact_attachments/%Y/%m/%d/',
                                 blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    is_processed = models.BooleanField('Обработано', default=False)

    class Meta:
        verbose_name = 'Контактное сообщение'
        verbose_name_plural = 'Контактные сообщения'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email} ({self.created_at.strftime("%d.%m.%Y %H:%M")})'

    def send_notification_email(self):
        subject = f'Новое контактное сообщение от {self.name}'
        message = f"""
        Получено новое сообщение:
        
        От: {self.name}
        Email: {self.email}
        Сообщение: {self.message}
        
        Время получения: {self.created_at.strftime("%d.%m.%Y %H:%M")}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )