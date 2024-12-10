from django.urls import path
from realestate import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('management/', views.management, name='management'),
    path('management/add/', views.add_development_view, name='add_development'),
     path('management/edit/<int:dev_id>/', views.edit_development, name='edit_development'),
    path('mobiledDwelling/', views.mobiledDwelling, name='mobiledDwelling'),
    path('mobileBuildings/', views.mobileBuildings, name='mobileBuildings'),
    path('mobileIndustries/', views.mobileIndustries, name='mobileIndustries'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)