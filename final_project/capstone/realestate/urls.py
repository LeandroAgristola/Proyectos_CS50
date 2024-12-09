from django.urls import path
from realestate import views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path('management/', views.admin_development_view, name='management'),
    path('mobiledDwelling/', views.mobiledDwelling, name='mobiledDwelling'),
    path('mobileBuildings/', views.mobileBuildings, name='mobileBuildings'),
    path('mobileIndustries/', views.mobileIndustries, name='mobileIndustries'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)