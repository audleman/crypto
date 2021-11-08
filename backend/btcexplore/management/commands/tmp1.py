
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block, Transaction
from btcexplore.services import bitcoinrpc
from django.core.paginator import Paginator
from django.db import transaction
from collections import defaultdict
from btcexplore.utils.vin import get_vin_type, VinType
from btcexplore.utils.vout import get_vout_type, VoutType
from pprint import pprint as pp

class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    def handle(self, *args, **options):
        
        print(bitcoinrpc.get_block_hash(708415))
        # unprocessed_blocks = Block.objects.filter(processed=False).order_by('height')
        # for block in unprocessed_blocks:
        #     print(block)
        #     for tx in block.extended_data['tx']:
        #         for vout in tx['vout']:
        #             try:
        #                 if (
        #                     vout['scriptPubKey']['type'] == 'nulldata' or
        #                     'OP_RETURN' in vout['scriptPubKey']['asm']
        #                 ):
                            
        #                     pp(vout)
        #                     import ipdb; ipdb.set_trace()
        #             except Exception as e:
        #                 pp(e)
        #                 import ipdb; ipdb.set_trace()
                
                
                    