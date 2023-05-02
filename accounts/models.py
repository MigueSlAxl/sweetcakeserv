from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1) 
    rut = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ntelefono = models.CharField(max_length=15, blank=True, null=True)
    nemergencia = models.CharField(max_length=15, blank=True, null=True)
    local = models.CharField(max_length=50, blank=True, null=True)
    # Info del registro
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha ingreso")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualizacion")
    deleted_at =  models.DateTimeField(auto_now=False, verbose_name="Fecha eliminacion", blank=True, null=True)