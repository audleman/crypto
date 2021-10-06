
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block, Transaction
from btcexplore.services import bitcoinrpc
from django.core.paginator import Paginator
from django.db import transaction
from collections import defaultdict
from btcexplore.utils.vin import get_vin_type, VinType
from btcexplore.utils.vout import get_vout_type, VoutType


class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    def handle(self, *args, **options):
        types = defaultdict(int)
        for block in Block.objects.all().order_by('height'):
            for tx in block.extended_data['tx']:
                for vout in tx['vout']:
                    try:
                        tt = get_vout_type(vout)
                        types[tt] += 1
                        if tt == VoutType.NONSTANDARD:
                            import ipdb; ipdb.set_trace()
                    except Exception:
                        from pprint import pprint as pp
                        print('Unhandled vout format')
                        pp(vout)
                        import ipdb; ipdb.set_trace()
                    
            if block.height and block.height % 100 == 0:
                print(block, types)
            
            
                    