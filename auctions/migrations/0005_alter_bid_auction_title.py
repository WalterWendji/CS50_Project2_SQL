# Generated by Django 4.2.11 on 2025-02-26 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_auction_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='auction_title',
            field=models.CharField(max_length=30),
        ),
    ]
