from django.db import models
from btcexplore.services import bitcoinrpcservice


# Create your models here.
class Block(models.Model):

    height = models.PositiveIntegerField(unique=True)

    hash = models.CharField(max_length=64, unique=True)

    # data = models.JSONField()

    @property    
    def data(self):
        if not hasattr(self, '__data'):
            self.__data = bitcoinrpcservice.get_block(self.hash)
        return self.__data

    transactions_created = models.BooleanField(default=False)

    def __str__(self):
        return f'<Block: {self.data["height"]}>'

    class Meta:

        db_table = 'block'



class Transaction(models.Model):

    # Non-unique
    # https://bitcoin.stackexchange.com/questions/11999/can-the-outputs-of-transactions-with-duplicate-hashes-be-spent
    txid = models.CharField(max_length=64)

    hash = models.CharField(max_length=64)

    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='transactions')

    @property    
    def data(self):
        if not hasattr(self, '__data'):
            self.__data = bitcoinrpcservice.get_transaction(self.txid, self.block.hash)
        return self.__data

    class Meta:

        db_table = 'transaction'
