from django import forms
from .models import Contact
import os

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш email'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше сообщение',
                'rows': 5
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            if attachment.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 5 МБ')
            
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(attachment.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError('Поддерживаются только изображения (jpg, jpeg, png, gif)')
        
        return attachment