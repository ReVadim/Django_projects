from django.db import models
from django.contrib.auth.models import AbstractUser
from .services import get_timestamp_path


class AdvUser(AbstractUser):
    """ Custom user model
    """
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_message = models.BooleanField(default=True, verbose_name="Слать сообщения о новых комментариях?")

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Rubric(models.Model):
    """ Class Rubric
    """
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название рубрики')
    sequence_number = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок следования')
    super_rubric = models.ForeignKey(
        'SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')


class RubricDataManager(models.Manager):
    """ Rubric data manager
    """
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    """ Class SuperRubric
    """
    objects = RubricDataManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('sequence_number', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubric(Rubric):
    """ Class SubRubric
    """
    objects = RubricDataManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__sequence_number', 'super_rubric__name', 'sequence_number', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Advertisement(models.Model):
    """ Ads added by users
    """
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, max_length=9, verbose_name='Цена')
    contacts = models.CharField(max_length=300, verbose_name='Контакты')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def delete(self, *args, **kwargs):
        for _ in self.additionalimage_set.all():
            _.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    """ Additional illustrations from advertising
    """
    advert = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Дополнительная иллюстрация'
        verbose_name_plural = 'Дополнительные иллюстрации'
