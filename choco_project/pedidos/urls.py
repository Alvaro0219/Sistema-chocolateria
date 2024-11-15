from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]
