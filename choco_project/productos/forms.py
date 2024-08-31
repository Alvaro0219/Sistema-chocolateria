from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'precio', 'descripcion']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.instance_id = kwargs.get('instance', None).id if kwargs.get('instance') else None
        super(ProductoForm, self).__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Producto.objects.exclude(id=self.instance_id).filter(nombre=nombre).exists():
            raise forms.ValidationError("El nombre del producto ya está en uso. Por favor, elija otro.")
        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if Producto.objects.exclude(id=self.instance_id).filter(codigo=codigo).exists():
            raise forms.ValidationError("El código del producto ya está en uso. Por favor, elija otro.")
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        
        if self.request and not self.request.FILES.getlist('imagenes'):
            raise forms.ValidationError("Debes cargar al menos una imagen para el producto.")
        
        return cleaned_data

