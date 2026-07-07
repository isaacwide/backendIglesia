from django.db import models

class Cancion(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200, blank=True, null=True)
    letra = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['titulo']