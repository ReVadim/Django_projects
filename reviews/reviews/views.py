from django.http import HttpResponse
from django.shortcuts import render, reverse
import datetime
import os


def main_page_after_authentication_view(request):
    """ redirect page after authentication """

    return render(request, 'main_page.html')
