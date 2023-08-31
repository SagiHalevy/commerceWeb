from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionList(models.Model):
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name = "lists")
    productName = models.CharField(max_length=64)
    initialPrice = models.DecimalField(max_digits=30, decimal_places=2)
    info = models.TextField(max_length=1000)
    creationTime = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)
    productName = models.ForeignKey('AuctionList', on_delete=models.CASCADE, related_name = "bids")
    bidPrice = models.DecimalField(max_digits=30, decimal_places=2)
    lastBidTime = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    commenter = models.ForeignKey('User', on_delete=models.CASCADE)
    productName = models.ForeignKey('AuctionList', on_delete=models.CASCADE, related_name = "comments")
    creationTime = models.DateTimeField(auto_now_add=True)  
    comment = models.TextField(max_length=500)