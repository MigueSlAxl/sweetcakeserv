from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre=models.CharField(max_length=150,blank=False,null=False)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre

class Productos(models.Model):
    nombre=models.CharField(max_length=150,blank=False,null=False)
    precio=models.CharField(max_length=20,unique=True)
    fecha_elaboracion=models.DateField(auto_now=False,auto_now_add=False)
    fecha_vencimiento=models.DateField(auto_now=False,auto_now_add=False)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.nombre
    