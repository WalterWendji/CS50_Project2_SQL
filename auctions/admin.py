from django.contrib import admin

from .models import AuctionListing, Bid, Comment, Watchlist, User

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'start_bid', 'created_by', 'created_at', "is_closed")

class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'auction_title', 'bid_amount', 'bid_time', 'is_bidder_winner')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'auction')
        
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter_id', 'comment_text', 'auction_listing', 'comment_time')
    
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(User)
