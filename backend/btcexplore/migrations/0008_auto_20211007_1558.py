# Generated by Django 3.2.7 on 2021-10-07 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btcexplore', '0007_auto_20211007_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='total_received',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='total_sent',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='tx_count',
        ),
    ]
