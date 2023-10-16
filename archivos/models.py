from django.db import models

class Producto(models.Model):
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=255)  # Almacena la ruta de la imagen

    def __str__(self):
        return self.descripcion
