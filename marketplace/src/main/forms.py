from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .apps import user_registered
from .models import AdvUser, SuperRubric, Advertisement, AdditionalImage


class ChangeUserInfoForm(forms.ModelForm):
    """ Change user information form
    """
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ['username', 'email', 'first_name', 'last_name', 'send_message']


class RegisterUserForm(forms.ModelForm):
    """ Form for new user registration
    """
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html()
    )
    confirm_password = forms.CharField(
        label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Повторите ввод пароля'
    )

    def clean_password(self):

        password = self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)

        return password

    def clean(self):

        super().clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            errors = {'confirm_password': ValidationError('Пароли не совпадают', code='password_mismatch')}

            raise ValidationError(errors)

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)

        return user

    class Meta:
        model = AdvUser
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'send_message']


class SuperRubricForm(forms.ModelForm):
    """ SuperRubric form
    """
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(), empty_label=None, label='Надрубрика', required=True
    )

    class Meta:
        model = SuperRubric
        fields = '__all__'


class SearchForm(forms.Form):
    """ Simple search form
    """
    keyword = forms.CharField(required=False, max_length=20, label='')


class AdvForm(forms.ModelForm):
    """ Form for entering a new ad
    """
    class Meta:
        model = Advertisement
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AdvertisementsFormSet = inlineformset_factory(Advertisement, AdditionalImage, fields='__all__')
