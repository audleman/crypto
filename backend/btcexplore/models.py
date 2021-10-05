from django.db import models
from btcexplore.services import bitcoinrpcservice
from django.core.serializers.json import DjangoJSONEncoder
from json import JSONDecoder
from decimal import Decimal


class Block(models.Model):

    height = models.PositiveIntegerField(unique=True)

    hash = models.CharField(max_length=64, unique=True)

    time = models.DateTimeField(null=True)

    # Linked list of blocks 
    last = models.OneToOneField('Block', related_name='next', on_delete=models.SET_NULL, null=True)

    transactions_created = models.BooleanField(default=False)

    @property    
    def data(self):
        if not hasattr(self, '__data') or self.__data is None:
            self.__data = self.get_data(1)
        return self.__data

    @property
    def extended_data(self):
        return self.get_data(2)

    def get_data(self, verbosity=1):
        return bitcoinrpcservice.get_block(self.hash, verbosity)

    def __str__(self):
        return f'Block: {self.height} {self.time:%Y-%m-%d %H:%M}'

    class Meta:
        db_table = 'block'


class Transaction(models.Model):

    # Non-unique
    # https://bitcoin.stackexchange.com/questions/11999/can-the-outputs-of-transactions-with-duplicate-hashes-be-spent
    txid = models.CharField(max_length=64)

    hash = models.CharField(max_length=64)

    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='transactions')

    vin = models.JSONField(encoder=DjangoJSONEncoder)

    class VoutDecoder(JSONDecoder):
        """
        Lame hack to decode decimal fields for a transaction's vout list
        TODO: learn how to use json decoders properly!
        """
        def decode(self, s):
            out = super().decode(s)
            for v in out:
                v['value'] = Decimal(v['value'])
            return out

    vout = models.JSONField(encoder=DjangoJSONEncoder, decoder=VoutDecoder)

    def __str__(self):
        return f'Transaction: {self.txid}'

    class Meta:

        db_table = 'transaction'


class Wallet(models.Model):

    address = models.CharField(max_length=64)

    balance = models.DecimalField(max_digits=15, decimal_places=8)


class Utxo(models.Model):

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
