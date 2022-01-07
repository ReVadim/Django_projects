from django import forms
from django.contrib.auth import get_user_model

from courses.models import EducationalProgram

User = get_user_model()


class LoginForm(forms.ModelForm):
    """ Login form """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError(f'User with login {email} not exist')
        if not user.check_password(password):
            raise forms.ValidationError('Wrong password')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    """ New user registration form """

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].label = 'Your address'
        self.fields['phone'].label = 'Phone number'
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm password'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain == 'net':
            raise forms.ValidationError('Registration for ".net" is denied')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('this name already exists')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("passwords don't match")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_staff = False
        user.username = self.cleaned_data['email'].split('@')[0]
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'address', 'phone']


class ChangeUserInfoForm(forms.ModelForm):
    """ Form for change user information """
    email = forms.EmailField(required=True, label='Your email')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')


# class AddCourseCommentsForm(forms.ModelForm):
#     """ Form for add comments and assessment for course """
#     class Meta:
#         model = EducationalProgram
#         fields = ['assessment', 'comment']


# class EducationalProgramUpdateForm(forms.ModelForm):
#     """ Form for add or update comments or assessment for course """
#
#     assessment = forms.CharField(required=False)
#     comment = forms.CharField(required=False)
#
#     class Meta:
#         model = EducationalProgram
#         fields = ['assessment', 'comment']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['assessment'].label = 'assessment'
#         self.fields['comment'].label = 'comment'
#
#     def clean(self):
#
#         self.assessment = self.cleaned_data['assessment']
#         self.comment = self.cleaned_data['comment']
#         if int(self.assessment) < 0 or int(self.assessment) > 5:
#             raise forms.ValidationError('Wrong assessment')
#         print('cleaned_data             ', self.cleaned_data)
#         return self.cleaned_data
#
#     def save(self, commit=True):
#         program = super().save(commit=False)
#         program.assessment = self.assessment
#         program.comment = self.comment
#         print('program         ', program)
#         if commit:
#             program.save()
#         return program
