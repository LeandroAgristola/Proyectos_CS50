from django.urls import path
from realestate import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path('mobileHousing/', views.mobileHousing, name='mobileHousing'),
    path('mobileBuildings/', views.mobileBuildings, name='mobileBuildings'),
    path('mobileIndustries/', views.mobileIndustries, name='mobileIndustries'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)