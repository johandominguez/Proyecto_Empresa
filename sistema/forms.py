from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory
from sistema.models import Producto, Proveedor, venta, Detalleventa , cliente



class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != 'estado':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != 'estado':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

class ventaForm(forms.ModelForm):

    class Meta:
        model = venta
        fields = ['cliente']

    def __init__(self, *args, **kwargs):
        super(ventaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class DetalleventaForm(forms.ModelForm):

    class Meta:
        model = Detalleventa
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DetalleventaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad == '':
            raise forms.ValidationError("Debe ingresar una cantidad valida")
        return cantidad

    def clean_precio_venta(self):
        precio = self.cleaned_data['precio_venta']
        if precio == '':
            raise forms.ValidationError("Debe ingresar un precio valido")
        return precio

DetalleventaFormSet = inlineformset_factory(venta, Detalleventa, form=DetalleventaForm, extra=4)

class clienteForm(forms.ModelForm):

    class Meta:
        model = cliente
        fields = ['identificación','nombre','apellido','telefono','dirección','correo_electronico']
    
    def __init__(self, *args, **kwargs):
        super(clienteForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != 'estado':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

