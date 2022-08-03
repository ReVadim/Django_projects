from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
import django.template
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

from src.main.forms import ChangeUserInfoForm
from src.main.models import AdvUser
from .forms import RegisterUserForm
from .services import signer


def index(request):
    """ display main page
    """
    return render(request, 'main/index.html')


def other_page(request, page):
    """ displaying pages from page id
    """
    try:
        template = get_template('main/' + page + '.html')
    except django.template.TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class MarketplaceLoginView(LoginView):
    """ Standard authentication model
    """
    template_name = 'main/login.html'


class MarketplaceLogoutView(LoginRequiredMixin, LogoutView):
    """ Standartd logout view
    """
    template_name = 'main/logout.html'


@login_required()
def profile(request):
    """ User profile page
    """
    return render(request, 'main/profile.html')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """ Class for change user information
    """
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('src.main:profile')
    success_message = 'Данные успешно изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class MarketplacePasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Change user password class
    """
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('src.main:profile')
    success_message = 'Пароль успешно изменен'


class RegisterUserView(CreateView):
    """ New user registration
    """
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('src.main:register_done')


class RegisterDoneView(TemplateView):
    """ Displays a message about successful registration
    """
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    """ User activation
    """
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """ Delete User View
    """
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('src.main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def by_rubric(request, pk):
    pass
