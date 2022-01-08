from django.conf import settings
from django.urls import path
from main.services import RegistrationView, MaterialsView
from main.views import LoginView, UserChangePasswordView, ChangeUserInfoView, profile
from .. import services
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('', services.index, name='index'),
    path('accounts/registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password/change/', UserChangePasswordView.as_view(), name='change_password'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='change_profile'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/materials/', MaterialsView.as_view(), name='materials'),
    path('courses/all/', services.CoursesListView.as_view(), name='course_list')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
