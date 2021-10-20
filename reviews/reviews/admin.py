from django.contrib import admin

from .models import Survey, Question, QuestionSurvey, QuestionChoice, Answer


admin.site.register(Survey)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(QuestionChoice)
admin.site.register(QuestionSurvey)
