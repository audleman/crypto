
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
        types = defaultdict(int)
        for block in Block.objects.all().order_by('height'):
            for tx in block.extended_data['tx']:
                for vout in tx['vout']:
                    try:
                        types[vout['scriptPubKey']['type']] += 1
                    except Exception as e:
                        import ipdb; ipdb.set_trace()
                        print('no type')
            if block.height % 100 == 0:
                print(types)
            
            
                    