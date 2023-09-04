from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



def user_directory_path(instance,filename):
    return f'auction_images/user_{instance.seller.id}/{filename}'

class AuctionList(models.Model):
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name = "lists")
    productName = models.CharField(max_length=64)
    initialPrice = models.DecimalField(max_digits=30, decimal_places=2)
    info = models.TextField(max_length=1000)
    creationTime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to= user_directory_path, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name = "watchlist")
    # Define choices for the auction status
    AUCTION_STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed')
    )
    status = models.CharField(
        max_length=10,
        choices=AUCTION_STATUS_CHOICES,
        default='active'  # Set the default status to 'active' when an auction is created.
    )


class Bid(models.Model):
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)
    productName = models.ForeignKey('AuctionList', on_delete=models.CASCADE, related_name = "bids")
    bidPrice = models.DecimalField(max_digits=30, decimal_places=2)
    lastBidTime = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    commenter = models.ForeignKey('User', on_delete=models.CASCADE)
    productName = models.ForeignKey('AuctionList', on_delete=models.CASCADE, related_name = "comments")
    creationTime = models.DateTimeField(auto_now_add=True)  
    comment = models.TextField(max_length=500)


