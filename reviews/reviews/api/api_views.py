from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from forms import LoginForm
from reviews.api.serializers import SurveySerializer
from reviews.models import Survey


class LoginView(View):
    """ functionality class for user authorization """

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/main_page')
        return render(request, 'login.html', {'form': form})


class SurveyViewSet(ModelViewSet):
    """ Create survey viewSet class """

    serializer_class = SurveySerializer
    http_method_names = ['GET', 'POST', 'PATCH', 'DELETE']

    def post(self, request):
        try:
            data = SurveySerializer(data=request.data)
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data
            if validated_data['start_time'] > validated_data['end_time']:
                raise Exception('Invalid end_date')
            survey = Survey(**validated_data)
            survey.save()
            return Response(SurveySerializer(survey).data)
        except Exception as ex:
            raise ParseError(ex)
