from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Stores the user's first name with a maximum length of 30 characters
    first_name = models.CharField(max_length=30)
    # Stores the user's last name with a maximum length of 30 characters
    last_name = models.CharField(max_length=30)
    # Optional profile picture for the user, stored in 'profile_pics/' directory
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
