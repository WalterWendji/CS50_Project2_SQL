# Generated by Django 4.2.11 on 2025-02-26 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_watchlist_auction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WatchList',
        ),
    ]
