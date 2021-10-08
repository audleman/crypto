
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block, Transaction, Wallet, Utxo
from btcexplore.services.transaction import process_vin, process_vout, is_invalid_transaction
from django.db.transaction import atomic


class Command(BaseCommand):
    help = 'Process transactions'
    
    def add_arguments(self, parser):
        parser.add_argument('-r', '--reset', action='store_true')

    def handle(self, *args, **options):
        if options['reset']:
            print('Resetting transactions onwards')
            # Start with a clean slate 
            Transaction.objects.all().delete()
            Utxo.objects.all().delete()
            Wallet.objects.all().delete()
            Block.objects.filter(processed=True).update(processed=False)
            print('Wiped!')
            return

        unprocessed_blocks = Block.objects.filter(processed=False).order_by('height')
        for block in unprocessed_blocks:
            # Atomic - if there's any trouble roll back the entire block
            with atomic():
                print(block, '\n', '-' * len(str(block)))
                for tx in block.extended_data['tx']:
                    if is_invalid_transaction(tx['txid'], block.height):
                        continue
                    transaction = Transaction.objects.create(
                        txid=tx['txid'],
                        block=block)
                    print('   ', transaction)
                    process_vin(transaction, tx['vin'])
                    process_vout(transaction, tx['vout'])
                    print ('')
                block.processed = True
                block.save()

                
                
            
            
                    