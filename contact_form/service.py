from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def share_by_email(self, request, pk=None):
        contact = self.get_object()
        recipient_email = request.data.get('email')
        
        if not recipient_email:
            return Response({'error': 'Email address is required'}, status=400)
            
        subject = f"Shared Contact Message from {contact.name}"
        message = f"""
        {request.user.get_full_name()} shared a contact message with you:
        
        From: {contact.name}
        Message: {contact.message}
        
        View online: {request.build_absolute_uri(f'/contact/share/{contact.id}/')}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            return Response({'status': 'Message shared successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)