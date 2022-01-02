from django.urls import path

from main.services import RegistrationView
from main.views import LoginView
from .. import services


urlpatterns = [
    path('', services.index, name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('courses/all/', services.CoursesListView.as_view(), name='course_list')
]
