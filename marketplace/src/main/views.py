from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse, Http404
import django.template
from django.template.loader import get_template


def index(request):
    """ display main page """
    return render(request, 'main/index.html')


def other_page(request, page):
    """ displaying pages from page id """
    try:
        template = get_template('main/' + page + '.html')
    except django.template.TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class MarketplaceLoginView(LoginView):
    """ Standard authentication model
    """
    template_name = 'main/login.html'
