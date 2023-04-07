from django.test import TestCase
from main.models import User
from .models import Materials, Course, CourseComment, CourseAssessment


class CourseTestCase(TestCase):
    def create_materials_for_courses(self):
        material_1 = Materials.objects.create(name='First material', description='test')
        material_2 = Materials.objects.create(name='Second material')
        material_3 = Materials.objects.create(name='Third material')
        self.material_a = material_1
        self.material_b = material_2
        self.material_c = material_3
        self.materials = Materials.objects.all()

    def create_courses(self):
        course_1 = Course.objects.create(name='Course_1')
        course_2 = Course.objects.create(name='Course_2', url='test_url')
        self.course_a = course_1
        self.course_b = course_2

    def setUp(self):
        self.create_materials_for_courses()
        self.create_courses()

    def test_materials_count(self):
        materials = Materials.objects.all()
        self.assertEqual(materials.count(), 3)

    def test_material_name(self):
        self.assertEqual(self.material_b.name, 'Second material')

    def test_course_count(self):
        courses = Course.objects.all()
        self.assertEqual(courses.count(), 2)

    def test_materials_exist(self):
        self.course_a.material.set(self.materials)
        material = self.course_a.material
        self.assertTrue(material.exists())
        self.assertEqual(material.count(), 3)

    def test_course_url(self):
        self.assertEqual(self.course_b.url, 'test_url')


class CommentTestCase(TestCase):
    """ Testing Course comment model """
    def create_user(self):
        self.user = User.objects.create(username='Admin', is_active=True)

    def setUp(self):
        self.create_user()
        course_1 = Course.objects.create(name='Course_1')
        comment_1 = CourseComment.objects.create(comment='comment_text', user=self.user, course=course_1)
        self.comment = comment_1

    def test_comment_count(self):
        comments = CourseComment.objects.all()
        self.assertEqual(comments.count(), 1)

    def test_comment_text(self):
        text = self.comment.comment
        self.assertEqual(text, 'comment_text')


class CourseAssessmentTestCase(TestCase):
    """ Testing Course Assessment """
    def create_user(self):
        self.user = User.objects.create(username='Admin', is_active=True)

    def create_course(self):
        course_1 = Course.objects.create(name='Course_1')
        course_2 = Course.objects.create(name='Course_2', url='test_url')
        self.course_a = course_1
        self.course_b = course_2

    def create_assessments(self):
        self.assessment_1 = CourseAssessment.objects.create(user=self.user, course=self.course_a, assessment=1)
        self.assessment_5 = CourseAssessment.objects.create(user=self.user, course=self.course_b, assessment=5)

    def setUp(self):
        self.create_user()
        self.create_course()
        self.create_assessments()

    def test_assessments_count(self):
        qs = CourseAssessment.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_course_assessment_value(self):
        assessment_1 = CourseAssessment.objects.get(course=self.course_a)
        assessment_5 = CourseAssessment.objects.get(course=self.course_b)
        self.assertEqual(assessment_1.assessment, 1)
        self.assertEqual(assessment_5.assessment, 5)

    def test_course_assessor(self):
        user = CourseAssessment.objects.get(course=self.course_a).user
        self.assertEqual(user, self.user)
