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

    CATEGORY_CHOICES = [
        ('Uncategorized', 'Select a category'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Home and Garden', 'Home and Garden'),
        ('Toys and Games', 'Toys and Games'),
        ('Books', 'Books'),
        ('Sports and Outdoors', 'Sports and Outdoors'),
        ('Automotive', 'Automotive'),
        ('Jewelry and Watches', 'Jewelry and Watches'),
        ('Collectibles', 'Collectibles'),
        ('Health and Beauty', 'Health and Beauty'),
        ('Music and Instruments', 'Music and Instruments'),
        ('Art and Crafts', 'Art and Crafts'),
        ('Food and Beverages', 'Food and Beverages'),
        ('Pets', 'Pets'),
        ('Travel and Experiences', 'Travel and Experiences'),
        ('Other', 'Other'),  
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Uncategorized',  
    )


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


class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name = "notifications")
    product = models.ForeignKey('AuctionList', on_delete=models.CASCADE)
    notificationTime = models.DateTimeField(auto_now_add=True)    
    is_read = models.BooleanField(default=False)