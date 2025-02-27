from django.contrib import admin

from .models import AuctionListing, Bid, Comment, Watchlist

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'created_by', 'created_at')

class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'auction_title', 'bid_amount', 'bid_time')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction')
        
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist, WatchlistAdmin)
