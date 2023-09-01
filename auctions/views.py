from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *


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
        'auctionLists': AuctionList.objects.all()
    })


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




def productPage():
    return render(request, "auctions/productPage.html")







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


