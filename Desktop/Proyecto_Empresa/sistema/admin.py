from __future__ import unicode_literals
from django.contrib.admin.models import LogEntry
from django.contrib import admin
from sistema.models import venta, Detalleventa,cliente, Producto, Proveedor 


# Register your models here.

class DetalleventaAdmin(admin.TabularInline):
    model = Detalleventa

class ventaAdmin(admin.ModelAdmin):
    inlines = [DetalleventaAdmin]
    list_display = ['cliente','fecha']

    search_fields = ['cliente','fecha']
    

class clienteAdmin(admin.ModelAdmin):
    list_display = ['identificación', 'nombre', 'apellido','dirección', 
    'telefono', 'correo_electronico', 'publish_date']

    search_fields = ['identificación', 'nombre']

    fieldsets =[
        (None, {'fields': ['identificación','nombre','apellido']}),
        ('Información de Contacto' , {'fields': ['telefono','dirección','correo_electronico']}),
    ]

class ProductoAdmin(admin.ModelAdmin):

    list_display = ['codigo', 'nombre', 'descripcion',
                    'stock', 'valor_unitario', 'proveedor', 'publish_date']

    search_fields = ['codigo', 'nombre']
    
    fields = [
        ('codigo','nombre'),
        'descripcion',
        ('stock', 'valor_unitario','proveedor'),
    ]


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['ruc', 'razon_social', 'direccion',
                    'telefono', 'correo', 'publish_date']

    search_fields = ['ruc', 'razon_social']
    
    fieldsets =[
        (None, {'fields': [('ruc','razon_social')]}),
        ('Información de Contacto' , {'fields': [('direccion','telefono'),'correo',]}),

    ]

admin.site.register(venta, ventaAdmin)
admin.site.register(cliente, clienteAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Proveedor,ProveedorAdmin)

# ---Limpiar el panel de actividades recientes del administrador--

#LogEntry.objects.all().delete()