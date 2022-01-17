from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Materials, EducationalProgram, CourseComment, CourseAssessment
from .permissions import IsUser
from .serializers import CourseSerializer, MaterialSerializer, ProgramSerializer, CommentSerializer,\
    CourseAssessmentSerializer
from ..forms import CourseAddCommentForm


class CoursesViewSet(ModelViewSet):
    """ ViewSet for all courses """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class MaterialViewSet(ModelViewSet):
    """ ViewSet for all materials """

    serializer_class = MaterialSerializer
    queryset = Materials.objects.all()

    def get_permissions(self):

        if self.action in ["create", "partial_update", 'destroy', "update"]:
            permissions = [IsAuthenticated]
        else:
            return []
        return [perm() for perm in permissions]


class ProgramViewSet(ModelViewSet):
    """ ViewSet for all programs """

    serializer_class = ProgramSerializer
    queryset = EducationalProgram.objects.all()
    permission_classes = [IsUser]


class CourseCommentViewSet(ModelViewSet):
    """ Comments for courses """

    serializer_class = CommentSerializer
    queryset = CourseComment.objects.all()


def add_comment(request, course_pk):

    form = CourseAddCommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.course_id = course_pk
        comment.user = request.user
        comment.save()
    return render(request, 'new_comment')


@login_required()
def delete_comment(request, comment_pk):
    """ delete comment """

    comment = CourseComment.objects.get(pk=comment_pk)
    course_pk = comment.course_id
    comment.delete()
    return show_comment(request, course_pk)


def show_comment(request, course_pk):
    """ Show all comments about course """
    try:
        comments = CourseComment.objects.filter(course_id=course_pk)
        course_name = Course.objects.get(pk=course_pk)
        context = {'comments': comments, 'course_name': course_name, 'course_pk': course_pk}
        return render(request, 'course/comments.html', context)
    except NoReverseMatch:
        return render(request, 'main/base.html')


class CourseAssessmentViewSet(ModelViewSet):
    """ Course Assessments """

    serializer_class = CourseAssessmentSerializer
    queryset = CourseAssessment.objects.all()
