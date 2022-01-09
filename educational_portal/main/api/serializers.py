from rest_framework import serializers
from courses.models import Course, Materials, EducationalProgram
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


class ProgramSerializer(serializers.ModelSerializer):
    """ serializer class for all educational programs """

    student = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = EducationalProgram
        fields = '__all__'
