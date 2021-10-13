from rest_framework import serializers
from billing.models import BankAccount, Holder


class BankAccountSerializer(serializers.ModelSerializer):
    """ Bank account serializer """

    account_name = serializers.CharField(max_length=150)
    is_active = serializers.BooleanField()
    overdraft = serializers.BooleanField()
    balance = serializers.DecimalField(max_digits=18, decimal_places=2)

    def create(self, validated_data):

        defaults = dict(
            account_name=validated_data['account_name'],
            is_active=validated_data['is_active'],
            overdraft=validated_data['overdraft'],
            balance=validated_data['balance']
        )
        BankAccount.objects.update_or_create(defaults=defaults, account_name=validated_data['account_name'])
        return BankAccount(**validated_data)

    class Meta:
        model = BankAccount
        fields = '__all__'


class HolderSerializer(serializers.ModelSerializer):
    """ User serializer """

    bank_account = BankAccountSerializer(read_only=True)

    class Meta:
        model = Holder
        fields = ['id', 'first_name', 'last_name', 'bank_account']
