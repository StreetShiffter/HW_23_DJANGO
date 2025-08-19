from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from .views import CustomLoginView, UserRegisterView, UserProfileView, UserProfileEditView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit'),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('loging/', CustomLoginView.as_view(), name="loging"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('email-confirm/<str:token>/', email_verification, name="email-confirm"),
]