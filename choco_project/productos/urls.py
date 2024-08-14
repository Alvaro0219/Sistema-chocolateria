from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.productos, name='productos'),
    path('agregar/', views.agg_productos, name='agg_productos'),
    path('<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
]
