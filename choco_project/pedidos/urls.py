from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pedidos'

urlpatterns = [
    path('', views.ultimos_pedidos, name='ultimos_pedidos'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('<int:pedido_id>/agregar/', views.agregar_producto, name='agregar_producto'),
    path('sumar/<int:producto_id>/', views.sumar_producto, name='sumar_producto'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('<int:pedido_id>/generar_qr/', views.generar_qr, name='generar_qr'),
    path('<int:pedido_id>/cancelar_pedido/', views.cancelar_pedido, name='cancelar_pedido'),
    path('<int:pedido_id>/generar_factura/', views.generar_qr, name='generar_factura')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
