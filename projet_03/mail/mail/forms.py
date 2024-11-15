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
        editing = kwargs.get('instance') is not None
        super().__init__(*args, **kwargs)

        if editing:
            self.fields.pop("email")

        # Añadir la clase 'form-control' a cada campo
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture")

        if not profile_picture:
            return profile_picture

        if profile_picture.content_type not in ["image/jpeg", "image/png"]:
            raise ValidationError("Solo se permiten imágenes JPEG y PNG.")

        max_size_kb = 2048  # 2 MB en KB
        if profile_picture.size > max_size_kb * 1024:
            raise ValidationError(f"El tamaño máximo de la imagen es de {max_size_kb / 1024} MB.")

        return profile_picture

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.instance.pk:  # Si el usuario aún no existe en la base de datos
            user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
