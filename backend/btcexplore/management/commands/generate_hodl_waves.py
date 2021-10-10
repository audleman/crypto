
from typing import OrderedDict
from django.core.management.base import BaseCommand
from btcexplore.models import Utxo, HODLWave
from django.core.paginator import Paginator
from datetime import date, timedelta
from btcexplore.services.utxo import utxo_age_band

BATCH_SIZE = 1000

class Command(BaseCommand):
    help = 'Parse UTXOs into HODL waves'

    def handle(self, *args, **options):
        HODLWave.objects.all().delete()
        hodl_waves = OrderedDict({h.date: h for h in HODLWave.objects.all().order_by('date')})
        
        paginator = Paginator(Utxo.objects.all().order_by('created'), BATCH_SIZE)
        print(f'Processing {paginator.count} UTXOs over {paginator.num_pages} batched')
        for page in range(1, paginator.num_pages + 1):
            print(f'Page: {page}')
            for utxo in paginator.page(page).object_list:
                start_date = utxo.created.date()
                end_date = utxo.spent.date() if utxo.spent is not None else date.today()
                curr_date = start_date
                while curr_date <= end_date:
                    if curr_date not in hodl_waves:
                        hodl_waves[curr_date] = HODLWave.objects.create(date=curr_date)
                    hodl = hodl_waves[curr_date]
                    band = utxo_age_band(utxo, curr_date)
                    setattr(hodl, f'band_{band.value}_count', getattr(hodl, f'band_{band.value}_count') + 1)
                    setattr(hodl, f'band_{band.value}_sum', getattr(hodl, f'band_{band.value}_sum') + utxo.value)
                    curr_date += timedelta(days=1)
            print('Saving page results to db...')
            [hw.save() for hw in hodl_waves.values()]


            
            
            
                    