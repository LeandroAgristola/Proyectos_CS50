from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, default='user/default_profile.jpg')
    followers = models.ManyToManyField(
        'self', related_name='following', symmetrical=False, blank=True
    )

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    