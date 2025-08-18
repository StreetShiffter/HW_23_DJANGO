from django.urls import path
from users.apps import UsersConfig
from .views import CustomLoginView, CustomLogoutView, UserRegisterView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('loging/', CustomLoginView.as_view(), name="loging"),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
]