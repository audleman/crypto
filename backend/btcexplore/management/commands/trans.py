
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block, Transaction
from pprint import pprint as pp
from btcexplore.services import bitcoinrpcservice
from django.core.paginator import Paginator
from django.db import transaction
from collections import defaultdict


class Command(BaseCommand):
    help = 'Process transactions'

    def process_vin(self, block, transaction):
        print(f'    vins: {len(transaction.vin)}')
        for i, vin in enumerate(transaction.vin):
            if 'coinbase' in vin.keys():
                print(f'        vin {i} coinbase')



    def handle(self, *args, **options):

        tt = Transaction.objects.all()[0]
        # Start with a clean slate 
        Transaction.objects.all().delete()

        for block in Block.objects.filter(transactions_created=False).order_by('height')[0:5]:
            for tx in block.extended_data['tx']:
                
                transaction = Transaction.objects.create(
                    block=block,
                    txid=tx['txid'],
                    hash=tx['hash'],
                    vin=tx['vin'],
                    vout=tx['vout']
                )
                print(transaction)
                # import ipdb; ipdb.set_trace()

                self.process_vin(block, transaction)

                # Iterate 'vin' and process 
                #   - Mark Utxo's as spent
                #   - If Transaction fully spent, delete it
                #   - Gather statistics on transactions spent (spent age bands?)

                # Get or create wallet


                # Create UTXOs

                
                
            
            
                    