
from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.views import View
from django.urls import reverse_lazy

class UserRegisterView(View):
    '''Контроллер регистрации'''
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

class UserProfileView(View):
    '''Контроллер отображение профиля'''
    template_name = 'profile.html'


class CustomLoginView(LoginView):
    '''Контроллер входа в профиль'''
    template_name = 'loging.html'
    success_url = reverse_lazy('users:profile')

class CustomLogoutView(View):
    '''Контроллер выхода из профиля'''
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.INFO, 'Вы успешно вышли.')
        return redirect('catalog:home')
