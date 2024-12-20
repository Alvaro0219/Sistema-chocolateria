from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, ProductoImagen
from .forms import ProductoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import os
from choco_project.utils import es_admin_o_empleado, es_administrador

@login_required
@user_passes_test(es_admin_o_empleado)
def productos(request):
    productos = Producto.objects.all()
    # Obtener el término de búsqueda desde la barra de búsqueda
    query = request.GET.get('q')
    if query:
        # Filtrar productos que contengan el término de búsqueda en el nombre o descripción
        productos = productos.filter(nombre__icontains=query)

    return render(request, 'productos/productos.html', {'productos': productos})

@login_required
@user_passes_test(es_administrador)
def agg_productos(request):
    # Verifica si la solicitud es de tipo POST, lo que indica que se está enviando un formulario.
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            producto = form.save()
            for img in request.FILES.getlist('imagenes'):
                ProductoImagen.objects.create(producto=producto, imagen=img)
            messages.success(request, "Producto agregado exitosamente")
            return redirect('productos:productos')
        else:
            # Manejo de mensajes de error
            if form.has_error('nombre'):
                messages.error(request, "El nombre del producto ya está en uso. Por favor, elija otro.")
            elif form.has_error('codigo'):
                messages.error(request, "El código del producto ya está en uso. Por favor, elija otro.")
            elif form.non_field_errors():
                messages.error(request, form.non_field_errors())
            else:
                messages.error(request, "Por favor, completa todos los campos requeridos correctamente.")
    else:
        # Si la solicitud no es de tipo POST (probablemente GET), se crea una instancia vacía del formulario.
        form = ProductoForm()

    return render(request, 'productos/agg_productos.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

@login_required
@user_passes_test(es_administrador)
def editar_producto(request, pk):
    # Obtener el producto por su ID, o lanzar un 404 si no existe
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        # Pasar los datos del formulario junto con los archivos subidos y la instancia del producto
        form = ProductoForm(request.POST, request.FILES, instance=producto, request=request)
        
        if form.is_valid():
            # Guardar el producto con los nuevos cambios
            producto = form.save()
            
            # Manejar las nuevas imágenes, si las hay
            if request.FILES.getlist('imagenes'):
                # Eliminar imágenes anteriores solo si se suben nuevas
                ProductoImagen.objects.filter(producto=producto).delete()
                for img in request.FILES.getlist('imagenes'):
                    ProductoImagen.objects.create(producto=producto, imagen=img)
            
            messages.success(request, "Producto actualizado exitosamente")
            return redirect('productos:detalle_producto', pk=pk)  # Redirigir al detalle del producto
        else:
            # Manejo de mensajes de error
            if form.has_error('nombre'):
                messages.error(request, "El nombre del producto ya está en uso. Por favor, elija otro.")
            elif form.has_error('codigo'):
                messages.error(request, "El código del producto ya está en uso. Por favor, elija otro.")
            elif form.non_field_errors():
                messages.error(request, form.non_field_errors())
            else:
                messages.error(request, "Por favor, completa todos los campos requeridos correctamente.")
    else:
        # Inicializar el formulario con los datos actuales del producto
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
@user_passes_test(es_administrador)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Eliminar imágenes asociadas
        for imagen in producto.imagenes.all():
            if os.path.isfile(imagen.imagen.path):
                os.remove(imagen.imagen.path)
        
        # Eliminar el producto
        producto.delete()
        messages.success(request, "Producto eliminado exitosamente.")
        return redirect('productos:productos')
    
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

