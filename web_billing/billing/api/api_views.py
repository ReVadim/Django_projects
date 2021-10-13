from django.http import HttpResponse

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from billing.api.serializers import BankAccountSerializer, HolderSerializer
from billing.models import BankAccount, Holder


class CreateBankAccountViewSet(ModelViewSet):
    """ Create bank account """

    serializer_class = BankAccountSerializer
    http_method_names = ['post']


class BalanceView(ListAPIView):
    """ View balance information """

    serializer_class = BankAccountSerializer

    def get(self, request, *args, **kwargs):

        balance = float
        account_name = request.GET.get('account_name')

        account = BankAccount.objects.filter(account_name=account_name)
        for value in account:
            balance = value.balance
        return HttpResponse(balance)


class HoldersView(ListAPIView):
    """ Users information """

    serializer_class = HolderSerializer
    queryset = Holder.objects.all()


class AccountsView(ListAPIView):
    """ Bank Account List """

    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
