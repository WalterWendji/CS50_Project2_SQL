# Generated by Django 4.2.11 on 2025-02-26 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_watchlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='auction',
        ),
    ]
