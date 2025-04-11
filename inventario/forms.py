from django import forms
from .models import (
    Categoria, Proveedor, Producto, 
    Adquisicion, DetalleAdquisicion, 
    Entrega, DetalleEntrega
)
from django.forms import inlineformset_factory

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion', 'rut', 'activo']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'descripcion', 'categoria', 
            'proveedor_principal', 'precio_costo', 'precio_venta',
            'stock_minimo', 'ubicacion', 'imagen', 'activo'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class AjusteStockForm(forms.Form):
    cantidad = forms.IntegerField(label='Cantidad')
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        label='Motivo del ajuste'
    )

class AdquisicionForm(forms.ModelForm):
    class Meta:
        model = Adquisicion
        fields = ['numero_factura', 'proveedor', 'fecha', 'observaciones']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class DetalleAdquisicionForm(forms.ModelForm):
    class Meta:
        model = DetalleAdquisicion
        fields = ['producto', 'cantidad', 'precio_unitario']

DetalleAdquisicionFormset = inlineformset_factory(
    Adquisicion, 
    DetalleAdquisicion, 
    form=DetalleAdquisicionForm,
    extra=1,
    can_delete=True
)

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['destinatario', 'departamento', 'fecha', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class DetalleEntregaForm(forms.ModelForm):
    class Meta:
        model = DetalleEntrega
        fields = ['producto', 'cantidad']

DetalleEntregaFormset = inlineformset_factory(
    Entrega, 
    DetalleEntrega, 
    form=DetalleEntregaForm,
    extra=1,
    can_delete=True
)

class FechaRangoForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Fecha de inicio'
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Fecha de fin'
    )

class ProductoFilterForm(forms.Form):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre o código'}))
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías"
    )
    stock_bajo = forms.BooleanField(required=False, label="Solo stock bajo")