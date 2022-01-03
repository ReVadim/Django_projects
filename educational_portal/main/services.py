from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django import views
from django.views.generic import ListView

from courses.models import Course
from .forms import RegistrationForm
from django.http import HttpResponseRedirect


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


def index(request):
    """ Main page """
    return render(request, template_name='main/index.html',
                  context={'title': 'Courses', 'text': 'Welcome to our educational portal'})


class CoursesListView(ListView):
    """ Class Base View """
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'
    extra_context = {'title': 'list of all educational programs'}

