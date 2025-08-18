from django import forms
from validate_email import validate_email
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'image', 'phone', 'country']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Проверка формата email
            if not validate_email(email):
                raise forms.ValidationError('Введите корректный email-адрес.')

            # # Дополнительная проверка домена (опционально)
            # blocked_domains = ['mail.ru', 'disposable.com']
            # domain = email.split('@')[1]
            # if domain in blocked_domains:
            #     raise forms.ValidationError('Этот email-сервис не поддерживается.')
        return email

