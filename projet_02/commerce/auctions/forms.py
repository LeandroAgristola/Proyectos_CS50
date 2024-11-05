from django import forms
from .models import AuctionListing, Bid, Comment, Category

# Form for creating a new auction listing
class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing  # Specifies the model to use for this form
        fields = ['title', 'description', 'starting_bid', 'image', 'category']  # Fields to include in the form
        labels = {  # Labels for the form fields
            'title': 'Title',
            'description': 'Description',
            'starting_bid': 'Starting Bid',
            'image': 'Image (optional)',  # Changed to 'Image (optional)'
            'category': 'Category',
        }
        widgets = {  # Customizes the widgets for the form fields
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Sets the description field as a textarea with specified rows and columns
        }

# Form for placing a bid
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid  # Specifies the model to use for this form
        fields = ['bid_amount']  # Field to include in the form
        labels = {  # Labels for the form fields
            'bid_amount': 'Bid Amount',  # Translated to English
        }
        widgets = {  # Customizes the widgets for the form fields
            'bid_amount': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),  # Sets the bid amount field as a number input with minimum and step values
        }

# Form for adding a comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Specifies the model to use for this form
        fields = ['content']  # Field to include in the form
        labels = {  # Labels for the form fields
            'content': 'Comment',  # Translated to English
        }
        widgets = {  # Customizes the widgets for the form fields
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'form-control'}),  # Sets the content field as a textarea with specified rows and columns, and adds a Bootstrap class
        }