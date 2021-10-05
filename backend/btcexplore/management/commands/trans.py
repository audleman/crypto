
from django.core.management.base import BaseCommand, CommandError
import ipdb
from btcexplore.models import Block, Transaction

from btcexplore.utils.address_conversion import address_from_public_key


class Command(BaseCommand):
    help = 'Process transactions'


    def process_vin(self, block, transaction):
        print(f'    vins: {len(transaction.vin)}')
        for i, vin in enumerate(transaction.vin):
            if 'coinbase' in vin.keys():
                print(f'        vin {i} coinbase')


    def process_vout(self, block, transaction):
        print(f'    vouts: {len(transaction.vout)}')
        for vout in transaction.vout:
            if vout['scriptPubKey']['type'] == 'pubkey':
                address = address_from_public_key(vout['scriptPubKey']['asm'].split(' ')[0])                
                print(f'    value: {vout["value"]} to address: {address}')


    def handle(self, *args, **options):

        # Start with a clean slate 
        Transaction.objects.all().delete()

        for block in Block.objects.filter(transactions_created=False).order_by('height')[0:5]:

            print(f'{block}\n----------------------------------------------------------------')
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

                self.process_vout(block, transaction)

                print ('')

                # Iterate 'vin' and process 
                #   - Mark Utxo's as spent
                #   - If Transaction fully spent, delete it
                #   - Gather statistics on transactions spent (spent age bands?)

                # Get or create wallet


                # Create UTXOs

                
                
            
            
                    