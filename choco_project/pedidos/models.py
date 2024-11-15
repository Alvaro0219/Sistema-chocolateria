from django.db import models
from productos.models import Producto  # Asumiendo que ya tienes esta app

class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cajero = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Asume que el usuario es un cajero o admin
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    imagen = models.ImageField(upload_to='pedidos/', blank=True, null=True)  # Imagen cargada para reconocimiento

    def __str__(self):
        return f"Pedido {self.id} - {self.fecha}"

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.productos.all())
        self.save()

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def precio_unitario(self):
        return self.producto.precio

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
