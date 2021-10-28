from django.db import models
from model_utils import Choices
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator


class TimestampFields(models.Model):
    """ Date and time information """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='updated_at')

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """ Mixin for user management """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
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
                        ('BUYER', _('buyer')),
                        ('SHOP_MANAGER', _('shop_manager')),
                        )

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    objects = UserManager()
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(blank=True, null=True, max_length=100,
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
                                 default='BUYER',
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


class Shop(models.Model):
    """ List of stores """

    name = models.CharField(verbose_name='Title', max_length=155)
    url = models.URLField(verbose_name='URL_link', max_length=255, null=True, blank=True)
    manager = models.OneToOneField(User,
                                   verbose_name='User',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE
                                   )

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = "Shop-list"

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Product categories """

    name = models.CharField(verbose_name='Category', max_length=100)
    shops = models.ManyToManyField(Shop,
                                   blank=True,
                                   related_name='categories',
                                   verbose_name='shops'
                                   )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "category-list"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Assortment of goods """

    category = models.ForeignKey(Category,
                                 verbose_name='category',
                                 related_name='products',
                                 blank=True, on_delete=models.CASCADE
                                 )
    name = models.CharField(verbose_name='product_tltle',
                            max_length=100
                            )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = "Product-list"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    """ Product detail: name, quantity, price and other """

    product = models.ForeignKey(Product,
                                verbose_name='product',
                                related_name='product_detail',
                                blank=True, on_delete=models.CASCADE
                                )
    shop = models.ForeignKey(Shop,
                             verbose_name='shop',
                             related_name='products_info',
                             blank=True, on_delete=models.CASCADE
                             )
    quantity = models.PositiveIntegerField(verbose_name='quantity',
                                           default=1,
                                           validators=[MinValueValidator(1)]
                                           )
    description = models.TextField(verbose_name='description',
                                   null=True
                                   )
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name='price',
                                validators=[MinValueValidator(0), MaxValueValidator(1_000_000)]
                                )
    price_retail = models.DecimalField(max_digits=9, decimal_places=2,
                                       verbose_name='retail_price',
                                       validators=[MinValueValidator(0), MaxValueValidator(1_000_000)]
                                       )

    class Meta:
        verbose_name = 'product detail'
        verbose_name_plural = 'products detail'
        # constraints = [
        #     models.UniqueConstraint(fields=['product', 'shop', 'description'], name='unique_product_info'),
        # ]


class Parameter(models.Model):
    """ Name of product parameter """

    parameter = models.CharField(verbose_name='product_parameter_name',
                                 max_length=50
                                 )

    class Meta:
        verbose_name = 'product parameter name'
        verbose_name_plural = "product parameters names"
        ordering = ('-parameter',)

    def __str__(self):
        return self.parameter


class ProductParameter(models.Model):
    """ Description of product parameters """

    product_info = models.ForeignKey(ProductInfo,
                                     verbose_name='product_info',
                                     related_name='product_parameters',
                                     blank=True, on_delete=models.CASCADE
                                     )
    parameter = models.ForeignKey(Parameter,
                                  verbose_name='parameter',
                                  related_name='product_parameter',
                                  blank=True, on_delete=models.CASCADE
                                  )
    value = models.CharField(verbose_name='product_parameter_value',
                             max_length=150
                             )

    class Meta:
        verbose_name = 'product parameter value'
        verbose_name_plural = "product parameters values"


class Order(TimestampFields, models.Model):
    """ Class of orders """

    STATUS = Choices(
                    ('NEW', _('new order')),
                    ('CONFIRM', _('confirmed')),
                    ('IN_PROGRESS', _('in progress')),
                    ('ASSEMBLED', _('assembled')),
                    ('SENT', _('sent')),
                    ('DELIVERED', _('delivery')),
                    ('DONE', _('fully completed')),
                    ('CANCELED', _('canceled')),
                    )

    user = models.ForeignKey(User,
                             verbose_name='user',
                             related_name='user_order',
                             on_delete=models.CASCADE
                             )
    date = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    order_state = models.TextField(choices=STATUS,
                                   default='NEW',
                                   verbose_name='order_state'
                                   )
    contact = models.ForeignKey('Contact', blank=True, null=True,
                                on_delete=models.CASCADE, verbose_name='contact')

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.date} from {self.user}'


class OrderItem(models.Model):
    """ Order detail """

    order = models.ForeignKey(Order,
                              verbose_name='order_information',
                              related_name='order_detail',
                              blank=True, on_delete=models.CASCADE
                              )
    product = models.ForeignKey(Product,
                                verbose_name='product_in_order',
                                related_name='product_info',
                                blank=True, on_delete=models.CASCADE
                                )
    shop = models.ForeignKey(Shop,
                             verbose_name='product_in_shop',
                             related_name='shop_info',
                             blank=True, on_delete=models.CASCADE
                             )
    quantity = models.PositiveIntegerField(verbose_name='quantity',
                                           default=1,
                                           validators=[MinValueValidator(1)]
                                           )
    product_info = models.ForeignKey(ProductInfo, verbose_name='product detail',
                                     related_name='ordered_items',
                                     blank=True, on_delete=models.CASCADE
                                     )

    class Meta:
        verbose_name = 'order detail'
        verbose_name_plural = 'orders detail'


class Contact(models.Model):
    """ User detail information. Contact list."""

    user = models.ForeignKey(User,
                             verbose_name='user',
                             related_name='user_contact',
                             blank=True, on_delete=models.CASCADE
                             )
    country = models.CharField(verbose_name='country', max_length=50)
    city = models.CharField(verbose_name='city', max_length=50)
    street = models.CharField(verbose_name='street', max_length=80)
    house = models.PositiveIntegerField(verbose_name='house',
                                        blank=True,
                                        validators=[MinValueValidator(1)]
                                        )
    structure = models.CharField(verbose_name='struct',
                                 blank=True, max_length=10
                                 )
    building = models.CharField(verbose_name='building',
                                blank=True, max_length=10
                                )
    apartment = models.CharField(verbose_name='apartment',
                                 blank=True, null=True, max_length=20)
    phone = models.CharField(verbose_name='phone_number',
                             unique=True, max_length=20
                             )

    class Meta:
        verbose_name = 'Contact_info'
        verbose_name_plural = 'Contacts_info'


class ConfirmEmailToken(TimestampFields, models.Model):
    """ Confirm Email Token class """

    @staticmethod
    def generate_secret_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    user_token = models.CharField(
        _("user_token"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.user_token:
            self.user_token = self.generate_secret_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return f"Password reset token for user {self.user}"

    class Meta:
        verbose_name = 'Confirm Email Token'
        verbose_name_plural = 'Confirm Email Token list'
