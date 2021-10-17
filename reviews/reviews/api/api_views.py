from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import login
from forms import LoginForm
from reviews.models import Survey
from django.contrib.auth import authenticate
from rest_framework.response import Response


from .serializers import SurveySerializer


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
    """ Survey ViewSet class """

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, request):
        return self.queryset

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


class SurveyView(APIView):
    get_queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def delete(self, request, survey_id):
        Survey.objects.get(id=survey_id).delete()
        return HttpResponse(f'<h1>Survey id={survey_id} DELETE</h1>')

    def patch(self, request, survey_id):
        change_object = Survey.objects.get(id=survey_id)
        change_object.title = request.data['title']
        change_object.description = request.data['description']
        change_object.save()
        return HttpResponse(change_object)
