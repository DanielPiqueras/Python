from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=200)
    edad = models.IntegerField()

    def __str__(self):
        devolver = f"{self.nombre}, {self.edad}"
        return devolver