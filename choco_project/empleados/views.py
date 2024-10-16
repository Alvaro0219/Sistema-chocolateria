from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from .forms import EmpleadoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from choco_project.utils import es_admin_o_empleado, es_administrador
from django.contrib import messages
from django.contrib.auth.hashers import make_password

@login_required
@user_passes_test(es_administrador)
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            # Crear un nuevo usuario empleado
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data['password'])
            usuario.save()
            
            # Asignar el usuario al grupo "empleados"
            grupo_empleados = Group.objects.get(name='Empleados')
            usuario.groups.add(grupo_empleados)

            messages.success(request, "Empleado creado exitosamente")
            return redirect('empleados:lista_empleados')
        else:
            messages.error(request, "Hubo un error al crear el empleado.")
    else:
        form = EmpleadoForm()

    return render(request, 'empleados/crear_empleado.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def lista_empleados(request):
    empleados = User.objects.filter(groups__name='Empleados')
    return render(request, 'empleados/lista_empleados.html', {'empleados': empleados})

def editar_empleado(request, pk):
    empleado = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado editado exitosamente")
            return redirect('empleados:lista_empleados')
        else:
            messages.error(request, "Por favor, completa todos los campos requeridos correctamente.")
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/editar_empleado.html', {'form': form, 'empleado': empleado})

def eliminar_empleado(request, pk):
    empleado = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, "Empleado eliminado exitosamente")
        return redirect('empleados:lista_empleados')
    return render(request, 'empleados/eliminar_empleado.html', {'empleado': empleado})