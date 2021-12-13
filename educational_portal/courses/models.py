from django.db import models

from main.models import User


class Course(models.Model):
    """ All courses class """

    name = models.CharField(verbose_name="title", max_length=100, unique=True)
    description = models.TextField(verbose_name="description", blank=True, null=True)
    url = models.URLField(verbose_name="URL_link", max_length=255, blank=True, null=True)
    image_files = models.FileField(upload_to='pdf_files/%Y-%m-%d/')
    course_owner = models.OneToOneField(User, verbose_name="owner", blank=True, null=True,
                                        on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name
