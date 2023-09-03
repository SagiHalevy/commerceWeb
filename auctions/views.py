from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .decorators import redirect_authenticated_user
from .models import *
from .util import *

class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title:")
    info = forms.CharField(
        label='Description:',
        widget=forms.Textarea(attrs={'rows': 15, 'cols':100})
    )
    price = forms.DecimalField(label="Starting Price:",min_value=0,  max_digits=30, decimal_places=2)
    image = forms.ImageField(label="Upload Image:", required=False)


def index(request):
    return render(request, "auctions/index.html",{
        # Adds to auctionLists extra field called 'highestBid' which equals to the Max() value of 
        # bidPrice in the relative_name table for "bids"
        'auctionLists': AuctionList.objects.annotate(highestBid = Max('bids__bidPrice')).order_by('creationTime')
    })


@login_required
def createListing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['info']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            auctionList = AuctionList(seller=request.user ,productName=title,
                                      initialPrice=price, info=description, image=image)
            auctionList.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createListing.html",{
        'form':CreateListingForm()
    })


def productPage(request, product_id): 
    product = get_object_or_404(AuctionList, pk=product_id)
    allProductBids = product.bids.all()
    state_message = request.session.pop('state_message', None) #state message - whether bid successed/failed
    highestBidder = (allProductBids.order_by("-bidPrice")[0].bidder) if allProductBids else None

    is_authenticated = request.user.is_authenticated
    in_watchlist = is_authenticated and request.user.watchlist.filter(pk=product.id).exists()   
    is_a_bidder = is_authenticated and allProductBids.filter(bidder=request.user).exists()
    userBid = is_authenticated and (allProductBids.filter(bidder=request.user).order_by("-bidPrice")[0].bidPrice) if is_a_bidder else None

    return render(request, "auctions/productPage.html",{
        'product':product,
        'bidPrice': getCurrentPrice(product),
        'state_message': state_message,
        'in_watchlist': in_watchlist,
        'highestBidder':highestBidder,
        'is_a_bidder':is_a_bidder,
        'userBid':userBid,
    })

@login_required
def submitBid(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(AuctionList, pk=product_id)
        try:
            userBidAmount = float(request.POST['bidAmount'])
        except ValueError:
            state_message = {'message': "ERROR: Invalid bid amount. Please enter a valid number.", 'accepted': False}
            request.session['state_message'] = state_message
            return HttpResponseRedirect(reverse("productPage", args=(product_id,)))


        highestPrice = getCurrentPrice(product) #highestPrice is the initialPrice, or the highest bid price (if exist)
        #using atomic transaction to avoid race condition
        with transaction.atomic():
            if userBidAmount > highestPrice:
                bid = Bid(bidder=request.user, productName=product, bidPrice=userBidAmount)
                bid.save()
                state_message = {'message':f"Success: Your bid of {userBidAmount}$ has been added to the auction.", 'accepted':True}
            else:
                state_message = {'message':f"ERROR: Your bid is too low! The highest bid at the moment is: {highestPrice}$", 'accepted':False}
                    
        request.session['state_message'] = state_message
        return HttpResponseRedirect(reverse("productPage",args=(product_id,)))


@login_required
def toggleWatchlist(request,product_id):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(AuctionList, pk=product_id) 
        action = request.POST.get('action', None)

        if action == 'addToWatchlist':
            if user not in product.watchlist.all():
                product.watchlist.add(user)
        elif action == 'removeFromWatchlist':
            if user in product.watchlist.all():
                product.watchlist.remove(user)

        return HttpResponseRedirect(reverse("productPage",args=(product_id,)))
     


@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request,"auctions/watchlist.html",{
        "watchlist":watchlist
    })














@redirect_authenticated_user
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

@redirect_authenticated_user
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


