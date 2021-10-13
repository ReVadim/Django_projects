from django.contrib import admin
from .models import Holder, BankAccount, Transaction

admin.site.register(Holder)
admin.site.register(BankAccount)
admin.site.register(Transaction)
