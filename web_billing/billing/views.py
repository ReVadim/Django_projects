import decimal

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from billing.forms import Payment
from billing.models import BankAccount, Transaction


def payment_operation(request):
    """ Processing the payment form using transaction """

    if request.method == 'POST':

        form = Payment(request.POST)

        if form.is_valid():

            donor_account = form.cleaned_data['donor']
            recipient_account = form.cleaned_data['recipient']
            amount = decimal.Decimal(form.cleaned_data['amount'])

        with transaction.atomic():

            donor = BankAccount.objects.select_for_update().get(account_name=donor_account)
            recipient = BankAccount.objects.select_for_update().get(account_name=recipient_account)

            donor.balance -= amount

            if (donor.balance < 0 and donor.overdraft) or donor.balance > 0:
                donor.save()
            else:
                transaction_status = Transaction(donor_account=donor,
                                                 recipient_account=recipient,
                                                 transfer_amount_rub=amount,
                                                 transfer_result=False)
                transaction_status.save()
                return HttpResponseRedirect('/')

            recipient.balance += amount
            recipient.save()

            transaction_status = Transaction(donor_account=donor,
                                             recipient_account=recipient,
                                             transfer_amount_rub=amount,
                                             transfer_result=True)
            transaction_status.save()
            return HttpResponseRedirect('/')

    else:
        form = Payment()

    return render(request, 'index.html', {'form': form})
