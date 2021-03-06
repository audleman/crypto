# Generated by Django 3.2.7 on 2021-10-07 03:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('btcexplore', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='transactions_created',
            new_name='processed',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='vin',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='vout',
        ),
        migrations.AddField(
            model_name='utxo',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 7, 3, 33, 41, 184273, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='utxo',
            name='spent',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='utxo',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[('1', 'Pubkey'), ('2', 'Pubkeyhash'), ('3', 'Nonstandard')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='utxo',
            name='id',
            field=models.CharField(max_length=70, primary_key=True, serialize=False),
        ),
    ]
