from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PedidoForm
from .models import Pedido, PedidoProducto
from django.urls import reverse
from .utils import reconocer_productos_por_segmento
from django.db import transaction
from productos.models import Producto


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
