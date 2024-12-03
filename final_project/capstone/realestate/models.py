from django.db import models

# Create your models here.

class development(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    image = models.ImageField(upload_to='developments')  
    brochurePaper = models.FileField(upload_to='developments_pdfs/')
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = 'development' 
        verbose_name_plural = 'developments' 

    def __str__(self):
        return self. title
