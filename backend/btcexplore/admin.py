from django.contrib import admin

from btcexplore.models import Block, Transaction


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass