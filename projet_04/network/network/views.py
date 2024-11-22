from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import User, Post
from django.core.paginator import Paginator


@login_required
def index(request):
    # Handle new post submission
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
    
    # Fetch all posts in reverse chronological order
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render page with paginated posts and form
    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": page_obj,
    })

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().order_by('-created_at')
    is_following = request.user.is_authenticated and profile_user.followers.filter(id=request.user.id).exists()

    if request.method == "POST" and request.user.is_authenticated:
        if request.user != profile_user:
            if is_following:
                profile_user.followers.remove(request.user)
            else:
                profile_user.followers.add(request.user)
            return redirect('profile', username=username)

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
    })

