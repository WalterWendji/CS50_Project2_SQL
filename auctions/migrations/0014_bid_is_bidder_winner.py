# Generated by Django 4.2.11 on 2025-03-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auctionlisting_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='is_bidder_winner',
            field=models.BooleanField(default=False),
        ),
    ]
