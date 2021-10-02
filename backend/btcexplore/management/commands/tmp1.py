
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block, Transaction
from pprint import pprint as pp
from btcexplore.services import bitcoinrpcservice
from django.core.paginator import Paginator
from django.db import transaction
from collections import defaultdict

class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    def handle(self, *args, **options):
        blocks = Block.objects.all()
    
        count = 0
        for block in blocks:
            tx_ids = block.data['tx']
            if len(tx_ids) != block.transactions.all().count():
                import ipdb; ipdb.set_trace()
            count += 1
            if count % 10000 == 0:
                print(count)
            
                    