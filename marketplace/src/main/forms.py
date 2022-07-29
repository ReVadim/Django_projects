from django import forms
from .models import AdvUser


class ChangeUserInfoForm(forms.ModelForm):
    """ Change user information form
    """
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ['username', 'email', 'first_name', 'last_name', 'send_message']

