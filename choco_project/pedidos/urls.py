from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('<int:pedido_id>/agregar/', views.agregar_producto, name='agregar_producto'),
    path('sumar/<int:producto_id>/', views.sumar_producto, name='sumar_producto'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]
