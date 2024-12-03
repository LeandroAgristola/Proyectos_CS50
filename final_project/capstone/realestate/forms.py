from django import forms
from django.core.exceptions import ValidationError
import re


def validateOnlyLetters(value):
    if not value.isalpha():
        raise ValidationError('This field must only contain letters.')

def validateOnlyLetters(value):
    if not re.match(r'^\d+$', value):
        raise ValidationError('The phone number should only contain numbers.')

class contactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        validators=[validateOnlyLetters],  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ethan'
        })
    )
    lastname = forms.CharField(
        max_length=100, 
        validators=[validateOnlyLetters], 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'James'
        })
    )
    phonenumber = forms.CharField(
        max_length=20,
        validators=[validateOnlyLetters],  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0115345456'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@djangomail.com'
        })
    )
    consultation = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Write your query here'
        })
    )
