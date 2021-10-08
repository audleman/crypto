from django.db import models
from btcexplore.services import bitcoinrpc
from django.core.serializers.json import DjangoJSONEncoder
from json import JSONDecoder
from decimal import Decimal
from django.utils import timezone
from btcexplore.utils.vout import VoutType
from django.db.models import Sum


GENESIS_TIME = '2009-01-03 10:15:05Z'


class Block(models.Model):

    height = models.PositiveIntegerField(unique=True)

    hash = models.CharField(max_length=64, unique=True)

    time = models.DateTimeField(null=True)

    # Linked list of blocks 
    last = models.OneToOneField('Block', related_name='next', on_delete=models.SET_NULL, null=True)

    processed = models.BooleanField(default=False)

    @property    
    def data(self):
        if not hasattr(self, '__data') or self.__data is None:
            self.__data = self.get_data(1)
        return self.__data

    @property
    def extended_data(self):
        return self.get_data(2)

    def get_data(self, verbosity=1):
        return bitcoinrpc.get_block(self.hash, verbosity)

    def __str__(self):
        return f'Block: {self.height} {timezone.localtime(self.time):%Y-%m-%d %H:%M}'


class Transaction(models.Model):

    txid = models.CharField(max_length=64, unique=True)

    block = models.ForeignKey(Block, on_delete=models.CASCADE)

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

    # vin = models.JSONField(encoder=DjangoJSONEncoder)
    # vout = models.JSONField(encoder=DjangoJSONEncoder, decoder=VoutDecoder)

    def __str__(self):
        return f'Transaction: {self.txid}'



class Wallet(models.Model):

    # Addresses are only 26-35 chars long, but pad for future-proofing
    address = models.CharField(max_length=64, unique=True)

    # balance = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    # tx_count = models.IntegerField(default=0)
    # total_received = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    # total_sent = models.DecimalField(max_digits=15, decimal_places=8, default=0)

    def __str__(self):
        # return f'Wallet: {self.address} bal: {self.balance} tx_count: {self.tx_count} recvd: {self.total_received} sent: {self.total_sent}'
        return f'Wallet: {self.address}'

    def get_balance(self):
        """ Balance is sum of unspent Utxos"""
        return self.utxo_set.filter(spent__isnull=True).aggregate(Sum('value'))['value__sum']


class Utxo(models.Model):

    # Concat: transaction_id + vout position. Should be 64 + 1-2 digits. Leaving 5 just in case
    id = models.CharField(max_length=70, primary_key=True)

    # Accounting, will eventually delete tx in/out
    tx_in = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='utxo_created_set')

    tx_out = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='utxo_spent_set', null=True)

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    # might be relevant when dealing w/ multisig
    type = models.PositiveSmallIntegerField(choices=VoutType.choices)

    value = models.DecimalField(max_digits=15, decimal_places=8)

    created = models.DateTimeField()

    spent = models.DateTimeField(null=True)

    def __str__(self):
        is_spent = '[SPENT]' if self.spent is not None else ''
        return f'Utxo: {self.id} {self.value} {is_spent}'
