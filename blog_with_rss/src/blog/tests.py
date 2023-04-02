from django.test import TestCase
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post


class PostTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('Test_user', 'test@email.com', '123')

        self.obj_1 = Post.objects.create(
            title='Test title', slug=slugify('Test title'),
            author=User.objects.first()
        )
        self.obj_2 = Post.objects.create(
            title='Another Test title', status=Post.Status.PUBLISHED,
            author=User.objects.first()
        )

    def test_valid_title(self):
        title = 'Test title'
        queryset = Post.objects.filter(title=title)
        self.assertTrue(queryset.exists())

    def test_slug_field(self):
        title = self.obj_1.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_1.slug)

    def test_created_count(self):
        queryset = Post.objects.all()
        self.assertEqual(queryset.count(), 2)

    def test_draft_case(self):
        qs = Post.objects.filter(status=Post.Status.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        qs = Post.objects.filter(status=Post.Status.PUBLISHED)
        now = timezone.now()
        published_qs = Post.objects.filter(publish__lte=now)
        self.assertTrue(published_qs.exists())
        self.assertEqual(qs.count(), 1)
