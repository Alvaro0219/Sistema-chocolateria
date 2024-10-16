from django.core.exceptions import PermissionDenied

# Verifica si el usuario es administrador
def es_administrador(user):
    if not user.is_superuser:
        raise PermissionDenied  # Lanza error 403 si no es administrador
    return True

# Verifica si el usuario es administrador o empleado
def es_admin_o_empleado(user):
    if not (user.is_superuser or user.groups.filter(name='Empleados').exists()):
        raise PermissionDenied  # Lanza error 403 si no es admin o empleado
    return True
