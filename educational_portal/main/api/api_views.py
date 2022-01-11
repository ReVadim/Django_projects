from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import ListAPIView
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


@login_required()
def add_comment(request, username, course_pk):

    form = CourseAddCommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.course_id = course_pk
        comment.user = request.user
        comment.save()
    return redirect('new_comment', user=username, course_id=course_pk)


def show_comment(request, course_pk):
    """ Show all comments about course """

    comments = CourseComment.objects.filter(course_id=course_pk)
    print('!'*30, comments)

    return render(request, 'course/comments.html', {'comments': comments})


class CourseAssessmentViewSet(ModelViewSet):
    """ Course Assessments """

    serializer_class = CourseAssessmentSerializer
    queryset = CourseAssessment.objects.all()
