from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText, FormActions, Field

from auctions.models import AuctionListing

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
class Listing(forms.ModelForm):
    title = forms.CharField(label="Title:", max_length=100, required=True)
    description = forms.CharField(label="Description:", max_length=300, widget=forms.Textarea, required=True)
    start_bid = forms.DecimalField(label="Starting Bid:", required=True)
    image_url = forms.URLField(label="Image's URL:", required=False)
    category = forms.ChoiceField(choices=CATEGORIES, label="Category:", required=True)
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-1'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'title', 
            'description', 
            AppendedText('start_bid', '$', active=True),
            Field('image_url', attrs={'required':False}), 
            'category',
            FormActions(
                Submit("create", "Create Listing")
            )
        )