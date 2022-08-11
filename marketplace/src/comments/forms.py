from captcha.fields import CaptchaField
from django import forms
from .models import Comment


class UserCommentForm(forms.ModelForm):
    """ A form for creating new comments on products by authorized users
    """
    class Meta:
        model = Comment
        exclude = ['is_active', ]
        widgets = {'advertisement': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    """ A form for creating new comments on products by unauthorized users
    """
    captcha = CaptchaField(label="Введите текст с картинки", error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ['is_active', ]
        widgets = {'advertisement': forms.HiddenInput}
