from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Materials, EducationalProgram
from .permissions import IsUser
from .serializers import CourseSerializer, MaterialSerializer, ProgramSerializer


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
