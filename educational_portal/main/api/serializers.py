from rest_framework import serializers
from courses.models import Course, Materials, EducationalProgram, CourseComment, CourseAssessment
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """ User contact information serializer """

    class Meta:
        model = User
        fields = ('username', 'user_type', 'email')


class MaterialSerializer(serializers.ModelSerializer):
    """ Material serializer for educational materials """

    name = serializers.CharField(required=True)

    class Meta:
        model = Materials
        fields = ['name', 'material']


class CourseSerializer(serializers.ModelSerializer):
    """ serializer class for all courses """

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    course_owner = UserSerializer()
    material = MaterialSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class BaseUserSerializer(serializers.ModelSerializer):
    """ Base serializer for user """

    user = UserSerializer()


class BaseCourseSerializer(serializers.ModelSerializer):
    """ Base serializer for course """

    course = CourseSerializer()


class ProgramSerializer(BaseCourseSerializer):
    """ serializer class for all educational programs """

    student = UserSerializer(read_only=True)

    class Meta:
        model = EducationalProgram
        fields = '__all__'


class CommentSerializer(BaseUserSerializer, BaseCourseSerializer):
    """ serializer class for all course comments """

    class Meta:
        model = CourseComment
        fields = '__all__'


class CourseAssessmentSerializer(BaseUserSerializer, BaseCourseSerializer):
    """ serializer class for all course assessments """

    class Meta:
        model = CourseAssessment
        fields = ['course', 'assessment']
