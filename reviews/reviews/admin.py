from django.contrib import admin

from .models import Survey, Question, QuestionSurvey, QuestionChoice


admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(QuestionChoice)
admin.site.register(QuestionSurvey)
