from django.db import models


class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    edad = models.IntegerField()
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE, default=1)

    def __str__(self):
        devolver = f"{self.nombre}, {self.edad}"
        return devolver


class Banco(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        devolver = f"{self.nombre}"
        return devolver
