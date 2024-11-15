from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PedidoForm
from .models import Pedido
from django.urls import reverse


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
    
    # Recalcula el total antes de renderizar, en caso de actualizaciones recientes
    pedido.calcular_total()
    
    context = {
        'pedido': pedido,
        'productos': pedido.productos.all(),  # Acceso a todos los productos del pedido
    }
    return render(request, 'pedidos/detalle_pedido.html', context)