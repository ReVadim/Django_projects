from django.urls import path

from main.services import RegistrationView
from main.views import LoginView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]
