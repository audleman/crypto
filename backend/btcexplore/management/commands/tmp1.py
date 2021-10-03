
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
        # unspent = bitcoinrpcservice.client.listunspent()
        b0 = Block.objects.get(height=0)
        b1 = Block.objects.get(height=1)
        import ipdb; ipdb.set_trace()
            
                    