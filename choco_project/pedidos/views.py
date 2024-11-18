from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PedidoForm
from .models import Pedido, PedidoProducto
from django.urls import reverse
from .utils import reconocer_productos_por_segmento
from django.db import transaction


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
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.imagen:
        try:
            productos_detectados = reconocer_productos_por_segmento(pedido.imagen.path)

            if not productos_detectados:
                messages.warning(request, "No se detectaron productos en la imagen.")
            else:
                with transaction.atomic():
                    for producto, cantidad in productos_detectados.items():
                        pedido_producto, creado = PedidoProducto.objects.get_or_create(
                            pedido=pedido,
                            producto=producto,
                            defaults={'cantidad': cantidad}
                        )
                        if not creado:
                            pedido_producto.cantidad += cantidad
                            pedido_producto.save()

                    pedido.calcular_total()

                messages.success(request, "Productos procesados correctamente.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar la imagen: {str(e)}")

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})
