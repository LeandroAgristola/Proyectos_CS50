from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Registrar el modelo de Usuario personalizado con el administrador predeterminado
admin.site.register(User, UserAdmin)