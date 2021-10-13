from django import forms


class Payment(forms.Form):
    """ Html form for transfer operations """

    donor = forms.CharField(max_length=30)
    recipient = forms.CharField(max_length=30)
    amount = forms.CharField(max_length=30)
