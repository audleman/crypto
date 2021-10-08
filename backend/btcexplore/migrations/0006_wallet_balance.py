# Generated by Django 3.2.7 on 2021-10-07 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcexplore', '0005_rename_transaction_count_wallet_tx_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=15),
        ),
    ]