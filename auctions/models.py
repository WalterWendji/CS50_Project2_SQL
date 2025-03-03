from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=30)
    imageURL = models.URLField(null=True, blank=True)
    #image = models.ImageField()
    category = models.CharField(max_length=30)
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
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.PROTECT) #The listing the comment is associated with
    comment_time = models.DateTimeField(auto_now_add=True)
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    auction = models.ForeignKey(AuctionListing, on_delete=models.PROTECT)
