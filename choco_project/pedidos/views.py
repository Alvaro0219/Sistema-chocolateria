from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PedidoForm
from .models import Pedido, PedidoProducto
from django.urls import reverse
from .utils import reconocer_productos_por_segmento
from django.db import transaction
from productos.models import Producto
import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def ultimos_pedidos(request):
    """
    Muestra los últimos 10 pedidos con un botón para crear un nuevo pedido.
    """
    ultimos_pedidos = Pedido.objects.order_by('-fecha')[:10]
    return render(request, 'pedidos/ultimos_pedidos.html', {'ultimos_pedidos': ultimos_pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cajero = request.user
            pedido.save()
            return redirect(reverse('pedidos:detalle_pedido', kwargs={'pedido_id': pedido.id}))
    else:
        form = PedidoForm()
    return render(request, 'pedidos/crear_pedido.html', {'form': form})

def detalle_pedido(request, pedido_id):
    """
    Muestra el detalle de un pedido y maneja el procesamiento de productos detectados
    solo la primera vez.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Asegurarnos de procesar la imagen solo si aún no se han detectado productos
    if pedido.imagen and not pedido.productos.exists():
        try:
            productos_detectados = reconocer_productos_por_segmento(pedido.imagen.path)

            if not productos_detectados:
                messages.warning(request, "No se detectaron productos en la imagen.")
            else:
                # Procesa los productos detectados
                with transaction.atomic():
                    for producto, cantidad in productos_detectados.items():
                        PedidoProducto.objects.get_or_create(
                            pedido=pedido,
                            producto=producto,
                            defaults={'cantidad': cantidad}
                        )

                    # Actualiza el total del pedido
                    pedido.calcular_total()

                messages.success(request, "Productos procesados correctamente.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar la imagen: {str(e)}")

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})

def sumar_producto(request, producto_id):
    """
    Incrementa la cantidad del producto en el pedido correspondiente.
    """
    producto_pedido = get_object_or_404(PedidoProducto, id=producto_id)
    producto_pedido.cantidad += 1
    producto_pedido.save()
    producto_pedido.pedido.calcular_total()  # Actualiza el total del pedido
    return redirect('pedidos:detalle_pedido', pedido_id=producto_pedido.pedido.id)

def restar_producto(request, producto_id):
    """
    Decrementa la cantidad del producto en el pedido, pero no permite cantidades menores a 1.
    """
    producto_pedido = get_object_or_404(PedidoProducto, id=producto_id)
    if producto_pedido.cantidad > 1:
        producto_pedido.cantidad -= 1
        producto_pedido.save()
        producto_pedido.pedido.calcular_total()  # Actualiza el total del pedido
    return redirect('pedidos:detalle_pedido', pedido_id=producto_pedido.pedido.id)


def eliminar_producto(request, producto_id):
    """
    Elimina un producto del pedido.
    """
    producto_pedido = get_object_or_404(PedidoProducto, id=producto_id)
    pedido_id = producto_pedido.pedido.id
    producto_pedido.delete()
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.calcular_total()  # Actualiza el total del pedido
    return redirect('pedidos:detalle_pedido', pedido_id=pedido_id)

def agregar_producto(request, pedido_id):
    """
    Agrega un nuevo producto al pedido o actualiza la cantidad si ya existe.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))
        producto = get_object_or_404(Producto, id=producto_id)

        pedido_producto, creado = PedidoProducto.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not creado:
            pedido_producto.cantidad += cantidad
            pedido_producto.save()
        pedido.calcular_total()  # Actualiza el total del pedido
        return redirect('pedidos:detalle_pedido', pedido_id=pedido.id)

    productos = Producto.objects.all()
    return render(request, 'pedidos/agregar_producto.html', {'productos': productos, 'pedido_id': pedido_id})

import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def generar_qr(request, pedido_id):
    # Crea el directorio si no existe
    temp_dir = os.path.join("media", "tmp")
    os.makedirs(temp_dir, exist_ok=True)

    # Define la ruta completa del archivo
    qr_file_path = os.path.join(temp_dir, "qr_temp.png")
    
    # Obtener el pedido
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Datos de la factura
    factura_data = (
        f"Pedido ID: {pedido.id}\n"
        f"Total: ${pedido.total}\n"
        f"Fecha: {pedido.fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"  # Formatear la fecha
        f"Cajero: {pedido.cajero.username}\n"
        f"Detalle del Pedido:\n"
    )
    for producto in pedido.productos.all():
        factura_data += (
            f" - {producto.producto.nombre}: {producto.cantidad} x ${producto.precio_unitario} "
            f"(Subtotal: ${producto.subtotal})\n"
        )

    # Crear el QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(factura_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Guardar el QR en un archivo temporal
    qr_img.save(qr_file_path)

    # Crear el PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Factura - Delicias ChocolaterIA")
    p.drawString(100, 735, f"Pedido ID: {pedido.id}")
    p.drawString(100, 720, f"Fecha: {pedido.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, 705, f"Cajero: {pedido.cajero.username}")
    p.drawString(100, 690, f"Total: ${pedido.total}")

    y_position = 675
    for producto in pedido.productos.all():
        p.drawString(
            100,
            y_position,
            f"{producto.producto.nombre}: {producto.cantidad} x ${producto.precio_unitario} "
            f"(Subtotal: ${producto.subtotal})",
        )
        y_position -= 20  # Aumentar el espacio entre renglones

    # Insertar el QR en la misma página
    p.drawImage(qr_file_path, 100, y_position - 220, width=200, height=200)  # Ajustar la posición del QR

    # Guardar el PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    # Enviar el PDF como respuesta HTTP
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=Factura_Pedido_{pedido.id}.pdf"
    return response
def cancelar_pedido(request, pedido_id):
    """
    Cancela el pedido y redirige al listado de pedidos.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    messages.success(request, "El pedido ha sido cancelado correctamente.")
    return redirect('pedidos:crear_pedido')
