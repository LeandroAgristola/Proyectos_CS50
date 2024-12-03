from django.db import models

# Create your models here.

class Desarrollo(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='desarrollos')  
    brochurePaper = models.FileField(upload_to='desarrollos_pdfs/')
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = 'desarrollo' 
        verbose_name_plural = 'desarrollos' 

    def __str__(self):
        return self.titulo
