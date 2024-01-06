from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from decimal import Decimal

from .models import User, Listing, Bid, Comment, Category

def index(request):
    active_listings = Listing.objects.all().filter(is_open=True)

    return render(request, "auctions/index.html", {
        "listings" : active_listings
    })


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

@login_required(login_url="login")
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":

        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image_url = request.POST["image_url"]
        category_name = request.POST["category"]
        listing_owner = request.user

        category = None
        if not Category.objects.all().filter(category_name=category_name):
            category = Category(
                category_name = category_name
            )
            category.save()
        else:
            category = Category.objects.all().get(category_name=category_name)

        listing = Listing(
            title=title, 
            description=description, 
            price=starting_price, 
            image_url=image_url,
            belongs_to_category=category,
            listing_owner=listing_owner,
        )
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")

def listing(request, listing_id):

    listing = Listing.objects.get(id=listing_id)

    if request.user.is_authenticated:

        #POST Handling
        if request.method == "POST":
            if request.POST.get("watchlist"):
                edit_watchlist(request, listing, listing_id)
            if request.POST.get("bid"):
                bid = Bid(
                    bid_amount = request.POST.get("bid"),
                    bid_owner = request.user,
                    bid_listing = listing,
                )
                bid.save()
            if request.POST.get("end"):
                end_listing(listing)
            if request.POST.get("comment"):
                create_comment(request.POST.get("comment"), listing, request.user)
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        #GET Handling

        biggest_bid = 0
        if listing.listing_bid.all().exists():
            biggest_bid = listing.listing_bid.all().aggregate(Max('bid_amount')).get('bid_amount__max')
        else:
            biggest_bid = listing.price
        min_bid = biggest_bid + Decimal(.01)

        return render(request, "auctions/listing.html", {
            "listing" : listing, 
            "watch_state" : request.user.watchlist.all().filter(id=listing_id).exists(),
            "biggest_bid" : biggest_bid,
            "min_bid" : min_bid,
            "user" : request.user,
            "comments": listing.comments.all()
        })
    else:
        #Guest Mode Listing Viewing
        return render(request, "auctions/listing.html", {
            "listing" : listing
        })

def edit_watchlist(request, listing, listing_id):
    watchlist = request.user.watchlist
    watch_state = watchlist.all().filter(id=listing_id).exists()
    if watch_state:
        watchlist.remove(listing)
    else:
        watchlist.add(listing)

def end_listing(listing):
    if listing.listing_bid.all():
        biggest_bid = listing.listing_bid.order_by('-bid_amount').first()
        biggest_bid_owner = biggest_bid.bid_owner

        #Make the user the winner of the listing
        listing.winning_user = biggest_bid_owner

    #close the listing
    listing.is_open = False
    listing.save()

def create_comment(message, listing, user):
    comment = Comment(message=message, belongs_to_listing=listing, belongs_to_user=user)
    comment.save()

@login_required(login_url="login")
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist" : request.user.watchlist.all()
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def category(request, category_name):
    listings_belonging_to_category = Category.objects.get(category_name=category_name).category_of_listing.all()
    return render(request, "auctions/category.html", {
        'listings_belonging_to_category' : listings_belonging_to_category,
        'category_name' : category_name
    })