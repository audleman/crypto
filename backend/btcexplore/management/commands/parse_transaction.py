
from django.core.management.base import BaseCommand, CommandError
from btcexplore.models import Block, Transaction
from pprint import pprint as pp

from django.core.paginator import Paginator
from django.db import transaction
from collections import defaultdict

class Command(BaseCommand):
    help = 'Query bitcoin node for new blocks'

    def handle(self, *args, **options):
        
        block = Block.objects.get(height=244160)
        
        trans = block.transactions.all()

        t = trans[0]
        import ipdb; ipdb.set_trace()
