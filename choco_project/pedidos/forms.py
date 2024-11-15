from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['imagen']  # Permitimos que solo se cargue una imagen inicialmente
