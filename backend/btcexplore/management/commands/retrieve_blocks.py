
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block
from pprint import pprint as pp
from btcexplore.services import bitcoinrpcservice



class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    # def add_arguments(self, parser):
    #     parser.add_argument('block_height', nargs=1, type=int, default=0)

    def add_genesis_block(self):
        block_hash = bitcoinrpcservice.get_block_hash(0)
        raw_block = bitcoinrpcservice.get_block(block_hash)
        block = Block.objects.create(
                height=raw_block['height'],
                hash=raw_block['hash'])

    def handle(self, *args, **options):

        if Block.objects.count() == 0:
            self.add_genesis_block()

        # Retrieve last block from db, see if we need to re-read it to get
        # the next block hash
        last_block = Block.objects.last()
        print(f'Last recorded block: {last_block}')
        raw_block = bitcoinrpcservice.get_block(last_block.hash)
        if 'nextblockhash' in raw_block:
            next_block_hash = raw_block['nextblockhash']
            print(f'Next hash found: {raw_block["nextblockhash"]}')
        else:
            print('No further blocks, we are at the tip')
            return
        
        # Read new blocks until we're at the tip
        while True:
            raw_block = bitcoinrpcservice.get_block(next_block_hash)
            
            block = Block.objects.create(
                height=raw_block['height'],
                hash=raw_block['hash'],
                last=last_block)
            print(f'{block} added with hash: {block.hash}')

            last_block = block

            if 'nextblockhash' in raw_block:
                next_block_hash = raw_block['nextblockhash']
            else:
                print(f'{block} is at the tip')
                break

                