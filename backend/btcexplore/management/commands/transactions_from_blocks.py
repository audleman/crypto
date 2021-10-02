
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
        paginator = Paginator(Block.objects.filter(transactions_created=False).order_by('pk'), 500)
        print(f'Processing {paginator.count} blocks over {paginator.num_pages} pages')
        for page in range(1, paginator.num_pages + 1):
            print(f'Page: {page}')
            tx_counts = defaultdict(int)
            # import ipdb; ipdb.set_trace()
            for block in paginator.page(page).object_list:
                tx_ids = block.raw_data['tx']
                tx_counts[block.height] = len(tx_ids)
                tx_batch = []
                for tx_id in tx_ids:
                    tx_batch.append(Transaction(txid=tx_id, block=block))
                with transaction.atomic():
                    Transaction.objects.bulk_create(tx_batch)
                    block.transactions_created = True
                    block.save()
            pp(tx_counts)
            
                    