# Generated by Django 3.2.7 on 2021-10-05 06:56

import btcexplore.models
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcexplore', '0011_auto_20211005_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='hash',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='txid',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='vin',
            field=models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='vout',
            field=models.JSONField(decoder=btcexplore.models.Transaction.VoutDecoder, encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
    ]