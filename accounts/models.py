from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect


class Profile(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,verbose_name='first_name')
    username = models.CharField(max_length=100,verbose_name='username')
    last_name = models.CharField(max_length=100,verbose_name='last_name')
    email = models.CharField(max_length=100,verbose_name='email')
    password = models.CharField(max_length=100,verbose_name='password')
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)
    def __str__(self):
        return self.user.username
    
    
    
    
    
    
    