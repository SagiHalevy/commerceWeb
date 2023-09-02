from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required
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
        'auctionLists': AuctionList.objects.annotate(highestBid = Max('bids__bidPrice'))
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
    state_message = request.session.pop('state_message', None) #state message - whether bid successed/failed
    product = AuctionList.objects.get(pk=product_id)
    return render(request, "auctions/productPage.html",{
        'product':product,
        'bidPrice': getCurrentPrice(product),
        'state_message': state_message
    })

@login_required
def submitBid(request, product_id):
    if request.method == 'POST':
        product = AuctionList.objects.get(pk=product_id)
        userBidAmount = float(request.POST['bidAmount'])
        highestPrice = getCurrentPrice(product) #highestPrice is the initialPrice, or the highest bid price (if exist)
        
        if userBidAmount > highestPrice:
            bid = Bid(bidder=request.user, productName=product, bidPrice=userBidAmount)
            bid.save()
            state_message = {'message':f"Success: Your bid of {userBidAmount}$ has been added to the auction.", 'accepted':True}
        else:
            state_message = {'message':f"ERROR: Your bid is too low! The highest bid at the moment is: {highestPrice}$", 'accepted':False}
                 
        request.session['state_message'] = state_message
        return HttpResponseRedirect(reverse("productPage",args=(product_id,)))




def addToWatchlist(request,product_id):
    pass








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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


