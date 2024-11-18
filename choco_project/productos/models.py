from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()

class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la imagen normalmente
        if self.imagen:
            self.procesar_imagen(self.imagen.path)

    def procesar_imagen(self, image_path):
        from PIL import Image
        with Image.open(image_path) as img:
            img = img.resize((300, 300))  # Ajustar tamaño sin convertir a escala de grises
            img.save(image_path)  # Sobrescribir la imagen procesada
