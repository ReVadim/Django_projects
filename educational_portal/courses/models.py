from django.core.validators import MaxValueValidator
from django.db import models

from main.models import User


class Course(models.Model):
    """ All courses class """

    name = models.CharField(verbose_name="title",
                            max_length=100,
                            unique=True)
    description = models.TextField(verbose_name="description",
                                   blank=True,
                                   null=True)
    url = models.URLField(verbose_name="URL_link",
                          max_length=255,
                          blank=True,
                          null=True)
    image_files = models.FileField(upload_to='pdf_files/%Y-%m-%d/')
    course_owner = models.ForeignKey(User, verbose_name="owner",
                                     blank=True,
                                     null=True,
                                     on_delete=models.DO_NOTHING)
    material = models.ForeignKey('Materials', on_delete=models.DO_NOTHING,
                                 blank=True,
                                 null=True,
                                 )

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = "course_storage"

    def __str__(self):
        return self.name


class TimestampFields(models.Model):
    """ Date and time information """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='updated_at')

    class Meta:
        abstract = True


class Materials(TimestampFields, models.Model):
    """  Educational materials for Courses"""

    name = models.CharField(max_length=50,
                            verbose_name='material'
                            )
    description = models.TextField(verbose_name='material_description',
                                   blank=True,
                                   null=True
                                   )
    material = models.FileField(verbose_name='file',
                                upload_to='materials/%Y-%m-%d/'
                                )

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        db_table = "material_storage"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class EducationalProgram(TimestampFields, models.Model):
    """ Students course list with materials and comments """
    student = models.OneToOneField(User, on_delete=models.CASCADE,
                                   verbose_name='student'
                                   )
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='course')
    assessment = models.PositiveIntegerField(verbose_name='assessment',
                                             default=1,
                                             validators=[MaxValueValidator(5)]
                                             )
    comment = models.TextField(null=True,
                               verbose_name='comment'
                               )

    class Meta:
        verbose_name = "program"
        verbose_name_plural = "programs"
        db_table = "program_storage"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.course} for {self.student}'
