from django import views
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from main.forms import LoginForm, ChangeUserInfoForm
from main.models import User


class LoginView(views.View):
    """ rendering registration form """

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'main/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'main/login.html', context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """ Change user information class """
    model = User
    template_name = 'account/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Changes success'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """ Change user password """
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Password successfully change'


@login_required
def profile(request):
    return render(request, 'account/profile.html')


# class CommentsView(LoginRequiredMixin, UpdateView):
#     """ Class for add or update comments or assessment for course """
#     model = EducationalProgram
#     template_name = 'course/add_comments.html'
#     form_class = EducationalProgramUpdateForm
#     # form_class = AddCourseCommentsForm
#     success_url = reverse_lazy('profile')
#     success_message = 'Changes success'
#
#     def setup(self, request, *args, **kwargs):
#         self.user_id = request.user.pk
#         print('pk' * 5, self.user_id)
#         return super().setup(request, *args, **kwargs)
#
#     def get_queryset(self):
#         queryset = EducationalProgram.objects.filter(student_id=self.user_id)
#         print('!'*15, queryset)
#         self._id = queryset.filter(course_id=1)
#         print('*' * 15, self._id)
#         return self.queryset
    #
    # def _setup(self, request, *args, **kwargs):
    #     query = self.get_queryset()
    #     q = query.filter(course_id=1).get(student_id=request.user.pk)
    #     self._id = q.pk
    #
    #     return super().setup(request, *args, **kwargs)
    #
    # def get_object(self, queryset=None):
    #     if not queryset:
    #         queryset = self.get_queryset()
    #
    #     return get_object_or_404(queryset, pk=self._id)

class CommentsView(views.View):
    """ Class for add or update comments or assessment for course """
    pass

#
# def edit_comment(request, id):
#     try:
#         comment = EducationalProgram.objects.get(id=id)
#         print('='*20, comment)
#
#     except:
#         return print('Nothing')

# def get(self, request, *args, **kwargs):
    #     form = EducationalProgramUpdateForm(request.POST or None)
    #     context = {
    #         'form': form
    #     }
    #     return render(request, 'course/add_comments.html', context)
    #
    # def post(self, request, *args, **kwargs):
    #     form = EducationalProgramUpdateForm(request.POST or None)
    #     print('/*/*/*/*/*/*', form)
    #     if form.is_valid():
    #         new_comment = form.save(commit=False)
    #         new_comment.assessment = form.cleaned_data['assessment']
    #         new_comment.comment = form.cleaned_data['comment']
    #         print('/*/*/*/*/*/*', new_comment)
    #         new_comment.save()
    #
    #         return HttpResponseRedirect('/')
    #
    #     context = {
    #         'form': form
    #     }
    #     return render(request, 'course/add_comments.html', context)

