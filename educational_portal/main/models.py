from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """ Mixin for user management """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ Create and save a user with the given username, email, and password. """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ Standard user model """

    USER_TYPE_CHOICE = (
                        ('STUDENT', _('student')),
                        ('ADMINISTRATOR', _('head_teacher')),
                        )

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    objects = UserManager()
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(blank=True,
                                null=True,
                                max_length=100,
                                validators=[username_validator],
                                error_messages={'unique': _("A user with that username already exists.")}
                                )
    is_active = models.BooleanField(_('active'),
                                    default=False,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. '
                                        'UnSelect this instead of deleting accounts.')
                                    )
    user_type = models.TextField(choices=USER_TYPE_CHOICE,
                                 default='STUDENT',
                                 verbose_name='user_type'
                                 )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users-list'

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
