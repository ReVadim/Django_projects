from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """ Form for sending Email
    """
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """ Comment form
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    """ Custom view to search posts
    """
    query = forms.CharField()
