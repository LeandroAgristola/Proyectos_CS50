from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile_picture", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        # Check if the instance is being edited by seeing if `instance` is provided
        editing = kwargs.get('instance') is not None
        super().__init__(*args, **kwargs)
        
        if editing:
            # If editing, remove the email field to prevent changes
            self.fields.pop("email")

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture")

        # Verificar si el campo es opcional y está vacío
        if not profile_picture:
            return profile_picture
        
        # Validar tipo de archivo de imagen
        if profile_picture.content_type not in ["image/jpeg", "image/png"]:
            raise ValidationError("Solo se permiten imágenes JPEG y PNG.")

        # Validar tamaño máximo de la imagen (2 MB en este ejemplo)
        max_size_kb = 2048  # 2 MB en KB
        if profile_picture.size > max_size_kb * 1024:
            raise ValidationError(f"El tamaño máximo de la imagen es de {max_size_kb / 1024} MB.")

        return profile_picture

    def save(self, commit=True):
        user = super().save(commit=False)
        # Solo asigna email como username en el caso de registro
        if not self.instance.pk:  # Si el usuario aún no existe en la base de datos
            user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
