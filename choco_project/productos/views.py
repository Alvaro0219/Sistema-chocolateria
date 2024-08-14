from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, ProductoImagen
from .forms import ProductoForm

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos.html', {'productos': productos})

def agg_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            for img in request.FILES.getlist('imagenes'):
                ProductoImagen.objects.create(producto=producto, imagen=img)
            return redirect('productos:productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/agg_productos.html', {'form': form})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:detalle_producto', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})
