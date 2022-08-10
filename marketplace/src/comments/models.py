from django.db import models
from django.utils.translation import gettext_lazy as _

from ..main.models import Advertisement


class Comment(models.Model):
    """ Comments for our ads
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name=_('advertisement'))
    author = models.CharField(max_length=30, verbose_name=_('author'))
    content = models.CharField(max_length=300, verbose_name=_('content'))
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_('show on display?'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('to publish?'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']
