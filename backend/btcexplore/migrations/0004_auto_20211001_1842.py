# Generated by Django 3.2.7 on 2021-10-01 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcexplore', '0003_remove_transaction_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='transactions_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='hash',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='txid',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]