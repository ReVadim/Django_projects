from django.urls import path
from main.services import RegistrationView
from main.views import LoginView, UserChangePasswordView
from .. import services
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', services.index, name='index'),
    path('accounts/registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password/change/', UserChangePasswordView.as_view(), name='change_password'),
    path('courses/all/', services.CoursesListView.as_view(), name='course_list')
]
