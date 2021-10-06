
from django.core.management.base import BaseCommand, CommandError
import ipdb
from btcexplore.models import Block, Transaction




class Command(BaseCommand):
    help = 'Process transactions'

    


    def handle(self, *args, **options):

        # Start with a clean slate 
        Transaction.objects.all().delete()

        for block in Block.objects.filter(transactions_created=False).order_by('height')[0:5]:

            print(f'{block}\n----------------------------------------------------------------')
            for tx in block.extended_data['tx']:
                
                transaction = Transaction.objects.create(
                    txid=tx['txid'],
                    block=block,
                    vin=tx['vin'],
                    vout=tx['vout'])

                print(transaction)

                transaction.process_vin(block, transaction)

                self.process_vout(block, transaction)

                print ('')

                # Iterate 'vin' and process 
                #   - Mark Utxo's as spent
                #   - If Transaction fully spent, delete it
                #   - Gather statistics on transactions spent (spent age bands?)

                # Get or create wallet


                # Create UTXOs

                
                
            
            
                    