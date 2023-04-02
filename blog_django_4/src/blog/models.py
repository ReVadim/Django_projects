from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """ Custom model manager
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """ Post model
    """
    class Status(models.TextChoices):
        """ choice Post status
        """
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name=_('title'))
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name=_('author'))
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, verbose_name=_('status'), choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('src.blog:post_detail', args=[self.publish.year,
                                                     self.publish.month,
                                                     self.publish.day,
                                                     self.slug])


class Comment(models.Model):
    """ Model for store users comments in post
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name=_('comments'))
    name = models.CharField(max_length=80, verbose_name=_('name'))
    email = models.EmailField()
    body = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
