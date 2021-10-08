
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block
from btcexplore.services import bitcoinrpc
from django.db import transaction
from datetime import datetime
import time
import pytz

timezone = pytz.timezone("UTC")
BATCH_SIZE = 1000


class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    # def add_arguments(self, parser):
    #     parser.add_argument('block_height', nargs=1, type=int, default=0)

    def add_genesis_block(self):
        """
        Loads the first block from the blockchain into our database
        """
        block_hash = bitcoinrpc.get_block_hash(0)
        raw_block = bitcoinrpc.get_block(block_hash)
        block = Block.objects.create(
                height=raw_block['height'],
                hash=raw_block['hash'],
                time=timezone.localize(datetime.fromtimestamp(raw_block['time'])))


    def create_block_batch(self, block_batch, last_block):
        """
        Bulk created a batch of blocks. After creation, we need to bulk update
        `last` field with a pointer to the pk of the previous block, which isn't
        available during the create
        """
        with transaction.atomic():
            start = time.time()
            created_blocks = Block.objects.bulk_create(block_batch)
            print(f'    batch insert took {(time.time() - start):.4f}s')
            # Populate last
            start = time.time()
            created_blocks[0].last = last_block
            for i in range(1, len(created_blocks)):
                created_blocks[i].last = created_blocks[i - 1]
            Block.objects.bulk_update(created_blocks, ['last'])
            print(f'    batch update took {(time.time() - start):.4f}s')

        return created_blocks


    def handle(self, *args, **options):

        # Block.objects.all().delete()

        if Block.objects.count() == 0:
            self.add_genesis_block()

        block_tip = bitcoinrpc.client.getblockcount()

        # Retrieve last block from db, see if we need to re-read it to get
        # the next block hash
        last_block = Block.objects.last()
        if last_block.height == block_tip:
            print(f'{last_block} already at the tip')
            return

        batch_count = 1
    
        while True:

            print(f'Batch {batch_count} starting at {last_block}')

            # Batch fetch blocks via RPC
            start = time.time()
            start_block = last_block.height + 1
            end_block = min(start_block + BATCH_SIZE + 1, block_tip)
            commands = [
                ['getblockhash', height] 
                for height in range(start_block, end_block + 1)]
            block_hashes = bitcoinrpc.client.batch_(commands)
            raw_blocks = bitcoinrpc.client.batch_([["getblock", h] for h in block_hashes])
            print(f'    {len(commands)} batched RPC calls in {(time.time() - start):.4f}s')
            
            # Create blocks in memory only
            block_batch = []
            for raw_block in raw_blocks:
                block_batch.append(Block(
                    height=raw_block['height'],
                    hash=raw_block['hash'],
                    time=timezone.localize(datetime.fromtimestamp(raw_block['time']))))

            created_blocks = self.create_block_batch(block_batch, last_block)

            # stats
            batch_count += 1
            print(f'    added {end_block - start_block} blocks {start_block} - {end_block}')

            # Loop control            
            last_block = created_blocks[-1]
            last_raw_block = raw_blocks[-1]
            if 'nextblockhash' not in last_raw_block:
                print(f'{last_block} is at the tip')
                return