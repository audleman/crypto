
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block
from pprint import pprint as pp
from btcexplore.services import bitcoinrpcservice



class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    # def add_arguments(self, parser):
    #     parser.add_argument('block_height', nargs=1, type=int, default=0)

    def handle(self, *args, **options):

        # Retrieve last block from db, see if we need to re-read it to get
        # the next block hash
        latest_block = Block.objects.last()
        print(f'Last recorded block: {latest_block}')
        if 'nextblockhash' not in latest_block.data:
            raw_block = bitcoinrpcservice.get_block(latest_block.hash)
            if 'nextblockhash' in raw_block:
                print(f'Next hash found: {raw_block["nextblockhash"]}')
                # Update record with new data
                latest_block.data = raw_block
                latest_block.save()
            else:
                print('No further blocks, we are at the tip')
                return
        block_hash = latest_block.data['nextblockhash']

        # Read new blocks until we're at the tip
        while True:            
            raw_block = bitcoinrpcservice.get_block(block_hash)
            block = Block.objects.create(
                height=raw_block['height'],
                hash=raw_block['hash'])
            print(f'{block} added with hash: {block.hash}')
            # pp(raw_block)

            if 'nextblockhash' in block.data:
                block_hash = block.data['nextblockhash']
            else:
                print(f'{block} is at the tip')
                break

                