from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from platformdirs import user_cache_dir 

from .forms import Listing

from .models import AuctionListing, Bid, User, Watchlist

auction_listings = AuctionListing.objects.all()
#watchlist = []

def index(request):
    return render(request, "auctions/index.html", {"auction_listings": auction_listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index", kwargs={"auction_listings": auction_listings}))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_new_listing(request):
    if request.method == "POST":
        form = Listing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            auction_listing = AuctionListing(
                title=title, 
                description=description, 
                price=start_bid, 
                imageURL=image_url, 
                category=category,
                created_by = request.user
                )

            auction_listing.save()
            print(f"save successfully: {auction_listing}")
            return HttpResponseRedirect(reverse("index", kwargs={"auction_listings": auction_listings}))
    else:
        form = Listing()
    return render(request, "auctions/newListing.html", {"form": form})


def show_listing(request, auction_id):
    auction = AuctionListing.objects.get(pk=auction_id)
    bid = ""
    bid_amounts = Bid.objects.filter(auction_listing=auction).values_list("bid_amount", flat=True)
    highest_bid = max(bid_amounts, default=0)
    
    message = perform_operation_for_watchlist_and_bid(request, bid, auction, auction_id, bid_amounts)       
    return render(request, "auctions/listing.html", {"auction":auction, "bid":bid, "message" : message, "bid_number": bid_amounts, "highest_bid": highest_bid})


def show_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).select_related("auction")
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})

def perform_operation_for_watchlist_and_bid(request, bid, auction, auction_id, bid_amounts):
    message = ""
    if request.method == "POST":
        if not request.user.is_authenticated:
            message = "Error: You should be logged in"
        else: 
            watchlist = Watchlist.objects.filter(user=request.user).select_related("auction")
            if auction in [item.auction for item in watchlist]:
                Watchlist.objects.get(user=request.user, auction=auction_id).delete()
            else:
                watch_element = Watchlist(
                    user = request.user,
                    auction = auction
                )
                watch_element.save()
                
            if request.POST.get("bid"):
                bid_user = float(request.POST.get("bid"))
                if bid_user >= auction.price and bid_user > max(bid_amounts, default=0):
                    bid = Bid(
                        bid_amount = bid_user,
                        bidder = request.user,
                        auction_listing = auction,
                        auction_title = auction.title
                    )
                    bid.save()
                else:
                    message = "Error: The bid should be at least as large as the starting bid, and must be greather than any other bid that have been placed!"
    return message 