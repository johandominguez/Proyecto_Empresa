from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Proveedor(models.Model):
    ruc = models.CharField(unique=True,max_length=11, blank=False, null=False)
    razon_social = models.CharField(max_length=150, blank=False, null=False)
    direccion = models.CharField(max_length=200, blank=False, null=False)
    telefono = models.CharField(max_length=15,null=True, blank=True)
    correo = models.EmailField(null=True,max_length=40, blank=True,
        help_text='Ejemplo: example@example.com // Opcional')
    publish_date = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'

    def __str__(self):
        return self.razon_social

class Producto(models.Model):
    codigo = models.CharField(max_length=15, blank=False, null=False, unique=True)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True, 
        help_text='Ingresa la descripción del producto aqui // Opcional')
    stock = models.IntegerField(blank=False, null=False, default=0)
    valor_unitario = models.IntegerField(blank =False, null=False,default = 0)
    estado = models.BooleanField(default=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,help_text='Ingresa aqui el respectivo proveedor del producto // Opcional', blank=True,null=True)
    publish_date =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class cliente (models.Model):
    identificación = models.CharField(max_length=10, blank=False, null=False , unique=True)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    dirección = models.CharField(max_length=50, blank=True, null=True)
    correo_electronico = models.EmailField(max_length=40, blank=True, 
        null=True, help_text='Ejemplo: example@example.com // Opcional')

    publish_date = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class venta(models.Model):
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE, blank=False, null=False)
    fecha = models.DateField(auto_now_add=True)
    
class Detalleventa(models.Model):
    venta = models.ForeignKey(venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio_venta = models.IntegerField(default=0)
    

