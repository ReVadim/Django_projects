from django.db import models
from django.contrib.auth import get_user_model


class StatusChoices(models.TextChoices):
    """ Question status choice """

    TEXT = 'TEXT_RESPONSE'
    ONE_CHOICE = 'ONE', 'ONE_CHOICE'
    MULTIPLE_CHOICE = 'MULTIPLE', 'MULTIPLE_CHOICE'


class Question(models.Model):
    """ List of Questions class """

    name = models.CharField(verbose_name='question_name', max_length=100)
    question_type = models.TextField(choices=StatusChoices.choices, default=StatusChoices.TEXT, verbose_name='type')
    question_text = models.TextField(verbose_name='question_text', null=True, blank=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f'{self.name} - {self.question_text}'


class QuestionChoice(models.Model):
    """ Acceptable answers to the question """

    question = models.ForeignKey(Question, related_name='question-choice', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100, default='input value', null=True)


class QuestionSurvey(models.Model):
    """ Questions in Survey linking table """

    question = models.ForeignKey(Question, related_name='question-list', on_delete=models.CASCADE)
    survey = models.ForeignKey('Survey', related_name='survey', on_delete=models.CASCADE, default=None)


class Survey(models.Model):
    """ Survey class, all information about surveys """

    title = models.CharField(verbose_name='title', max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='start_time')
    end_time = models.DateTimeField(auto_now_add=True, verbose_name='end_time')
    description = models.TextField(verbose_name='description')
    is_active = models.BooleanField(default=True)
    questions = models.ManyToManyField(Question, related_name='question', blank=True, through=QuestionSurvey)

    class Meta:
        verbose_name = 'Questionnaire'
        verbose_name_plural = 'Questionnaire-list'

    def __str__(self):
        return self.title


class Answer(models.Model):
    """ Answers to questions class, save data about the user's responses"""

    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    question_choice = models.ForeignKey(QuestionChoice, on_delete=models.DO_NOTHING, null=True)
    answer_owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.answer_text
