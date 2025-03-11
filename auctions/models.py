from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):

    CATEGORIES = (
        (None, "--please choose a category--"),
        ("antique_and_arts", "Antiques & Arts"),
        ("books", "Books"),
        ("cds_dvs_video_games", "CDs, DVD & Video Games"),
        ("clothing_and_accessories", "Clothing & Accessories"),
        ("computer_and_electronics", "Computer & Electronics"),
        ("food_wine_and_gourmet", "Food, Wine & Gourmet Itmes"),
        ("golf_and_sport_gear", "Golf & Sports Gear"),
        ("handbags_and_jewelry", "Handbags & Jewelry"),
        ("health_and_fitness", "Health & Fitness"),
        ("auto", "Auto"),
        ("home_and_garden", "Home & Garden"),
        ("toys", "Toys"),
    )

    title = models.CharField(max_length=30)
    imageURL = models.URLField(null=True, blank=True)
    category = models.CharField(choices=CATEGORIES, max_length=50)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)


class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    auction_title = models.CharField(max_length=30)
    bid_time = models.DateTimeField(auto_now_add=True)
    is_bidder_winner = models.BooleanField(default=False)


class Comment(models.Model):
    comment_text = models.TextField()
    commenter_id = models.ForeignKey(User, on_delete=models.PROTECT)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.PROTECT)
    comment_time = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    auction = models.ForeignKey(AuctionListing, on_delete=models.PROTECT)
