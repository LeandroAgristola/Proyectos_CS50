from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("following", views.following_view, name="following"),
    path("search/", views.search, name="search"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)