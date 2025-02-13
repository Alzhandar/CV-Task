from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import Contact
from django.shortcuts import get_object_or_404

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save()
            try:
                contact.send_notification_email()
                messages.success(request, 'Спасибо! Ваше сообщение успешно отправлено.')
            except Exception as e:
                messages.warning(request, 'Сообщение сохранено, но возникли проблемы с отправкой уведомления.')
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact_form/contact.html', {
        'form': form
    })

def share_view(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == "POST":
        recipient_email = request.POST.get('email')
        if recipient_email:
            try:
                subject = f"Shared Contact Message from {contact.name}"
                message = f"""
                Someone shared a contact message with you:
                
                From: {contact.name}
                Message: {contact.message}
                
                View online: {request.build_absolute_uri()}
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    fail_silently=False,
                )
                messages.success(request, 'Сообщение успешно отправлено!')
            except Exception as e:
                messages.error(request, 'Ошибка при отправке сообщения.')
        
    return render(request, 'contact_form/share.html', {'contact': contact})