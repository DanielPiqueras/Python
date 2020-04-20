from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Contacto(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=200)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
