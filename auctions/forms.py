from django import forms

from auctions.models import AuctionListing

class Listing(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=100, required=True)
    description = forms.CharField(label="Description", max_length=300, widget=forms.Textarea, required=True)
    start_bid = forms.DecimalField(label="Starting Bid in $", required=True)
    image_url = forms.URLField(label="Image's URL")
    category = forms.CharField(label="Category", max_length=50)
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
    