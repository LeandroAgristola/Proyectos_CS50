from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model that inherits from AbstractUser
class User(AbstractUser):
    pass  # Additional fields can be added here in the future.

# Model for auction listings
class AuctionListing(models.Model):
    CATEGORIES = [  # Category choices for auction listings
        ('fashion', 'Fashion'),  # 'fashion' is the key, 'Fashion' is the display label
        ('toys', 'Toys'),
        ('electronics', 'Electronics'),
        ('home', 'Home'),
    ]
    
    title = models.CharField(max_length=100)  # Title of the auction listing
    description = models.TextField()  # Description of the auction listing
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)  # Starting bid amount
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Current bid amount (optional)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Image for the listing (optional)
    category = models.CharField(max_length=20, choices=CATEGORIES, blank=True, null=True)  # Category of the listing (optional)
    active = models.BooleanField(default=True)  # Indicates if the listing is active
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")  # Owner of the listing
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the listing was created
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)  # Users who are watching this listing

    def __str__(self):
        return self.title  # String representation of the object (the title of the listing)

    def highest_bid(self):
        # Retrieve the highest bid for the listing
        highest_bid = self.bids.order_by('-bid_amount').first()  # Orders bids from highest to lowest
        return highest_bid.bid_amount if highest_bid else self.starting_bid  # Returns the highest bid amount or the starting bid if no bids exist

# Model for bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")  # User who placed the bid
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")  # Listing associated with the bid
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the bid
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the bid was placed

    def __str__(self):
        return f"{self.user} bid {self.bid_amount} on {self.listing.title}"  # String representation of the bid

# Model for comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # User who made the comment
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")  # Listing associated with the comment
    content = models.TextField()  # Content of the comment
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was made

    def __str__(self):
        return f"Comment by {self.user} on {self.listing.title}"  # String representation of the comment
