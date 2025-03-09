from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import AppendedText

from auctions.models import AuctionListing

class Listing(forms.ModelForm):
    title = forms.CharField(label="Title:", max_length=100, required=True)
    description = forms.CharField(label="Description:", max_length=300, widget=forms.Textarea, required=True)
    start_bid = forms.DecimalField(label="Starting Bid:", required=True)
    image_url = forms.URLField(label="Image's URL:")
    category = forms.CharField(label="Category:", max_length=50)
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'title', 
            'description', 
            AppendedText('start_bid', '$', active=True), 
            'image_url', 
            'category',
        )