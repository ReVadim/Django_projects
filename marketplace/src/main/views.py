from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
import django.template
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

from src.main.forms import ChangeUserInfoForm
from src.main.models import AdvUser


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
    template_name = 'main/password_change'
    success_url = reverse_lazy('src.main:profile')
    success_message = 'Пароль успешно изменен'
