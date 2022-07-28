from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from courses.models import Course
from main.forms import CourseAddCommentForm


@login_required()
def new_comment(request, username, course_id):
    """ Adding a comment to the course. Available only for registered users """

    course = get_object_or_404(Course.objects.select_related('name'), username=username, id=course_id)
    comment = course.comment.all()
    form = CourseAddCommentForm

    context = {
        'user': username,
        'course': course,
        'comment': comment,
        'form': form
    }
    return render(request, 'course/course_list.html', context)
