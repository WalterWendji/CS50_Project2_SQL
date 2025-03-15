from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import Listing
from .models import AuctionListing, Bid, User, Watchlist, Comment


def index(request):
    auction_listings = AuctionListing.objects.all()
    return render(
        request,
        "auctions/index.html",
        {
            "auction_listings": auction_listings,
            "highest_bids": give_the_highest_bid_of_each_item(),
        },
    )


def give_the_highest_bid_of_each_item():
    auction_listings = AuctionListing.objects.all()
    bid = Bid.objects.all()
    highest_bids = {}
    for listing_element in auction_listings:
        highest_bid = max(
            bid.filter(auction_listing=listing_element.id).values_list(
                "bid_amount", flat=True
            ),
            default=0,
        )
        highest_bids[listing_element.id] = (
            highest_bid if highest_bid else listing_element.start_bid
        )
    return highest_bids


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
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
            auction_listings = form.save(commit=False)
            auction_listings.created_by = request.user
            auction_listings.category = category
            auction_listings.imageURL = image_url
            auction_listings.save()
        
            return HttpResponseRedirect(reverse("index"))
    else:
        form = Listing()
    return render(request, "auctions/newListing.html", {"form": form})


def show_listing(request, auction_id):
    auction = AuctionListing.objects.get(pk=auction_id)
    
    is_user_creator = request.user == auction.created_by
    message = handle_watchlist_and_bid(request, auction, auction_id)
    
    auction.refresh_from_db()
    
    categories_list = dict(AuctionListing.CATEGORIES)
    
    bid_amounts = Bid.objects.filter(auction_listing=auction).values_list(
        "bid_amount", flat=True
    ).order_by('-bid_amount')
    bid_amount_to_be_displayed = bid_amounts[:3]
    highest_bid = max(bid_amounts, default=0)
    user_made_the_highest_bid = check_if_the_current_user_has_made_the_highest_bid(request, auction_id, highest_bid)
    close_auction(request, auction)
    bidder_won, winner_message = determine_auction_winner(request, auction_id, auction, highest_bid)
    
    comment_error_message = comment(request, auction)
    list_comment, user_list = show_comment_infos(auction)

    listing_parameters = {
        "auction": auction,
        "message": message,
        "bid_number": bid_amounts,
        "highest_bid": highest_bid,
        "is_user_creator": is_user_creator,
        "won_auction_message": winner_message,
        "got_winner": bidder_won,
        "list_comment": list_comment,
        "comment_error_message": comment_error_message,
        "user_list": user_list,
        "is_auction_in_watchlist": is_item_in_watchlist(request, auction),
        "categories_list": categories_list.items(),
        "user_made_the_highest_bid": user_made_the_highest_bid,
        "bid_amount_to_be_displayed":bid_amount_to_be_displayed,
    }
    return render(request, "auctions/listing.html", listing_parameters)


def show_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).select_related("auction")
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist, "highest_bids": give_the_highest_bid_of_each_item()})


def handle_watchlist_and_bid(request, auction, auction_id):
    message = ""
    if request.method == "POST":
        if not request.user.is_authenticated:
            return "Error: You should be logged in"
        handle_watchlist(request, auction, auction_id)
        if request.POST.get("bid"):
            message = handle_bid(request, auction)
    return message


def handle_watchlist(request, auction, auction_id):
    if request.POST.get("watchlist-element"):
        watchlist = Watchlist.objects.filter(user=request.user).select_related(
            "auction"
        )
        if auction in [item.auction for item in watchlist]:
            Watchlist.objects.get(user=request.user, auction=auction_id).delete()
        else:
            Watchlist.objects.create(user=request.user, auction=auction)


def handle_bid(request, auction):
    bid_amounts = Bid.objects.filter(auction_listing=auction).values_list(
        "bid_amount", flat=True
    )
    highest_bid = max(bid_amounts, default=0)
    bid_user = float(request.POST.get("bid"))
    
    if bid_user > auction.start_bid and bid_user > highest_bid:
        Bid.objects.create(
            bid_amount=bid_user,
            bidder=request.user,
            auction_listing=auction,
            auction_title=auction.title,
        )
        return ""
    else:
        return "Error: The bid should be at least as large as the starting bid, and must be greather than any other bid that have been placed!"


def close_auction(request, auction):
    if request.POST.get("close_auction"):
        auction.is_closed = True
        auction.save()
        
        

def determine_auction_winner(request, auction_id, auction, highest_bid):
    if Bid.objects.filter(auction_listing=auction_id).exists():
        if auction.is_closed:
            bids_made = Bid.objects.get(auction_listing=auction_id, bid_amount=highest_bid)
            bids_made.is_bidder_winner = True
            bids_made.save()
            
            if request.user == bids_made.bidder:
                winner_message = "Congratulation🥳!! You won the auction🎉!!"
            else:
                winner_message = f" {bids_made.bidder} won the auction 🦾"
            
            return True, winner_message
    
    return False, ""

# @login_required
def comment(request, auction):
    if request.method == "POST":
        if request.POST.get("comment"):
            if not request.user.is_authenticated:
                return "Error: You should be logged in"
            Comment.objects.create(
                comment_text=request.POST.get("comment"),
                commenter_id=request.user,
                auction_listing=auction,
            )

def show_comment_infos(auction):
    list_comment = ""
    user_list = ""
    if Comment.objects.exists():
        list_comment = Comment.objects.filter(auction_listing=auction).values(
            "comment_text", "commenter_id", "comment_time"
        )
        user_list = User.objects.values("id", "username")
    
    return list_comment, user_list


def show_categories(request):
    auctions = AuctionListing.objects.all()
    categories = set()
    categories_list = dict(AuctionListing.CATEGORIES)

    for auction_element in auctions:
        categories.add(auction_element.category)

    return render(
        request,
        "auctions/categories.html",
        {"categories": categories, "categories_list": categories_list.items()},
    )


def show_category_details(request, category_name):
    auctions_from_category = AuctionListing.objects.filter(category=category_name).all()
    selected_category = dict(AuctionListing.CATEGORIES).get(category_name)
    category_parameter = {
        "auctions_from_category": auctions_from_category,
        "category_name": selected_category,
        "highest_bids": give_the_highest_bid_of_each_item(),
    }
    return render(
        request,
        "auctions/category_details.html",
        category_parameter
    )

def is_item_in_watchlist(request, auction):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).select_related("auction")
        auction_list_from_watchlist = [item.auction for item in watchlist]
        if auction in auction_list_from_watchlist:
            return True
        else:
            return False
        
def check_if_the_current_user_has_made_the_highest_bid(request, auction_id, highest_bid):
    if request.user.is_authenticated:
        if Bid.objects.filter(bidder=request.user, auction_listing=auction_id):
            max_bid_from_the_current_user = max(Bid.objects.filter(bidder=request.user, auction_listing=auction_id).values_list("bid_amount", flat=True))
            user_made_bid = Bid.objects.filter(bidder=request.user, auction_listing=auction_id).exists()
            
            if user_made_bid and max_bid_from_the_current_user == highest_bid:
                return True
            else:
                return False