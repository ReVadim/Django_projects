from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from reviews.filters import AnswerFilter

from django.contrib.auth import login
from forms import LoginForm
from reviews.models import Survey, Question, Answer
from django.contrib.auth import authenticate
from rest_framework.response import Response


from .serializers import SurveySerializer, QuestionSerializer, AnswerSerializer


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
    permission_classes = [IsAdminUser]
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
    """ View for update or delete survey """

    get_queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, survey_id):
        Survey.objects.get(id=survey_id).delete()
        return HttpResponse(f'<h1>Survey id={survey_id} DELETE</h1>')

    def patch(self, request, survey_id):
        change_object = Survey.objects.get(id=survey_id)
        change_object.title = request.data['title']
        change_object.description = request.data['description']
        change_object.save()
        return HttpResponse(change_object)
    
    
class QuestionViewSet(ModelViewSet):
    """ ViewSet for questions """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]


class QuestionView(APIView):
    """ View for update or delete questions """

    get_queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def delete(self, request, question_id):
        Question.objects.get(id=question_id).delete()
        return HttpResponse(f'<h1>Question id={question_id} DELETE</h1>')

    def patch(self, request, question_id):
        change_object = Question.objects.get(id=question_id)
        change_object.name = request.data['name']
        change_object.question_type = request.data['question_type']
        change_object.question_text = request.data['question_text']
        change_object.save()
        return HttpResponse(change_object)


class AnswerView(APIView):
    """ Class for answers """

    get_queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filterset_class = AnswerFilter

    def get(self, request, user_id):
        return HttpResponse(Answer.objects.filter(answer_owner_id=user_id))

    def post(self, request):
        data = AnswerSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.validated_data
        answer = Answer(**validated_data)
        answer.save()
        return Response(SurveySerializer(answer).data)

    def patch(self, request, answer_id):
        change_object = Answer.objects.get(id=answer_id)
        change_object.answer_text = request.data['answer_text']
        change_object.save()
        return HttpResponse(change_object)

    def delete(self, request, answer_id):
        Answer.objects.get(id=answer_id).delete()
        return HttpResponse(f'<h1>Question id={answer_id} DELETE</h1>')
