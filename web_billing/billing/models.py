from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class BankAccount(models.Model):
    """ Bank account class """

    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(verbose_name='account_name', max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    is_active = models.BooleanField(default=False)
    overdraft = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='balance', default=0)

    class Meta:
        verbose_name = 'bank_account'
        verbose_name_plural = 'bank_account_list'

    def __str__(self):
        return f'account: {self.account_name} | balance: {self.balance}'


class Holder(AbstractUser, models.Model):
    """ Extended version of user model """

    bank_account = models.ForeignKey(BankAccount, verbose_name='bank_account', related_name='accounts', blank=True,
                                     null=True, on_delete=models.DO_NOTHING
                                     )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Transaction(models.Model):
    """ Bank transfers class """

    donor_account = models.ForeignKey(BankAccount,
                                      verbose_name='donor_account', related_name='donor', on_delete=models.PROTECT
                                      )
    recipient_account = models.ForeignKey(BankAccount,
                                          verbose_name='recipient_account', related_name='recipient',
                                          on_delete=models.PROTECT
                                          )
    transfer_amount_rub = models.DecimalField(max_digits=9, decimal_places=2,
                                              verbose_name='price',
                                              validators=[MinValueValidator(0)]
                                              )
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='transfer_at')
    transfer_result = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
