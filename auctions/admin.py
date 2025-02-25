from django.contrib import admin

from .models import AuctionListing, Bid, Comment

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'created_by', 'created_at')

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
