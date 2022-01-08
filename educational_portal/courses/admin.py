from django.contrib import admin
from .models import Course, Materials, EducationalProgram, CourseAssessment, CourseComment


admin.site.register(Course)
admin.site.register(Materials)
admin.site.register(EducationalProgram)
admin.site.register(CourseAssessment)
admin.site.register(CourseComment)
