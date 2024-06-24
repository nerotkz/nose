from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.shortcuts import render
from django.http import HttpResponse



class Registros(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=20,)
    correo = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = 'registros'

class Manga(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'mangas'


class MangaNuevo(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='mangas/', null=True, blank=True)
    class Meta:
        db_table = 'mangas_nuevos'
    def __str__(self):
        return self.nombre
