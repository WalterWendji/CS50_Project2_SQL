# Generated by Django 4.2.11 on 2025-02-26 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auctionlisting_image_auctionlisting_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='auction_title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
