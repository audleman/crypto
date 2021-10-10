from django.contrib import admin

from btcexplore.models import Block, Transaction, HODLWave


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass


@admin.register(HODLWave)
class HODLWaveAdmin(admin.ModelAdmin):
    
    list_display = (
        'date', 
        'band_1d_sum', 
        'band_1w_sum', 
        'band_1m_sum', 
        'band_3m_sum', 
        'band_6m_sum', 
        'band_1y_sum', 
        'band_2y_sum', 
        'band_3y_sum', 
        'band_5y_sum', 
        'band_7y_sum', 
        'band_10y_sum', 
        'band_over_10y_sum', 
    )