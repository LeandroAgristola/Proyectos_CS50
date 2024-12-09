from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import development
import re

def validateOnlyLetters(value):
    if not value.isalpha():
        raise ValidationError('This field must contain only letters.')

def validateOnlynumbers(value):
    if not re.match(r'^\d+$', value):
        raise ValidationError('The phone number must contain only numbers.')

def validateOnlyemail(value):
  try:
      validate = EmailValidator()
      validate(value)
  except ValidationError:
      raise ValidationError('Please enter a valid email.')  
  return True 

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
        validators=[validateOnlynumbers],  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0115345456'
        })
    )
    email = forms.EmailField(
        validators=[validateOnlyemail], 
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

class DevelopmentForm(forms.ModelForm):
    class Meta:
        model = development
        fields = ['title', 'content', 'image', 'brochurePaper']