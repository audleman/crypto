from django.db import models

# Create your models here.
class Block(models.Model):

    height = models.PositiveIntegerField()

    hash = models.CharField(max_length=64)

    data = models.JSONField()

    def __str__(self):
        return f'<Block: {self.data["height"]}>'

    class Meta:

        db_table = 'block'



class Transaction(models.Model):

    txid = models.CharField(max_length=64)

    hash = models.CharField(max_length=64)

    data = models.JSONField()

    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    class Meta:

        db_table = 'transaction'
