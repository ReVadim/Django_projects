from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from ..main.services import send_new_comment_notification

from ..main.models import Advertisement


class Comment(models.Model):
    """ Comments for our ads
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name=_('advertisement'))
    author = models.CharField(max_length=30, verbose_name=_('author'))
    content = models.CharField(max_length=300, verbose_name=_('content'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_('show on display?'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('published'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    """ Signal handler. Sends a message when a new comment appears
    """
    author = kwargs['instance'].advertisement.author
    if kwargs['created'] and author.send_message:
        send_new_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
