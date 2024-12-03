from django.contrib import admin
from .models import Desarrollo

# Register your models here.

class desarrolloAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated') 

admin.site.register(Desarrollo, desarrolloAdmin)
