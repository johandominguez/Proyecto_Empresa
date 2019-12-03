# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.edit import UpdateView, CreateView 
from django.views.generic.list import ListView
from sistema.forms import ProductoForm, ProveedorForm, ventaForm, DetalleventaFormSet, clienteForm 
from sistema.models import Producto, Proveedor, venta, Detalleventa, cliente
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.http.response import HttpResponseRedirect


from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from django.http import HttpResponse
from reportlab.lib.units import cm
from reportlab.platypus.tables import Table,TableStyle
from reportlab.lib import colors

# Create your views here.

class ListadoProductos(ListView):
    model = Producto
    template_name = 'productos.html'
    context_object_name = 'productos'

class ListadoClientes(ListView):
    model = cliente
    template_name = 'clientes.html'
    context_object_name = 'cliente'

class ListadoProveedores(ListView):
    model = Proveedor
    template_name = 'proveedores.html'
    context_object_name = 'proveedores'

class Listadoventas(ListView):
    model = venta
    template_name = 'ventas.html'
    context_object_name = 'ventas'

class CrearProducto(CreateView):
    template_name = 'producto.html'
    form_class = ProductoForm
    success_url = reverse_lazy('productos:listado_productos')

class CrearCliente(CreateView):
    template_name = 'cliente.html'
    form_class = clienteForm
    success_url = reverse_lazy('productos:listado_clientes')

class CrearProveedor(CreateView):
    template_name = 'proveedor.html'
    form_class = ProveedorForm
    success_url = reverse_lazy('productos:listado_proveedores')

class ModificarProducto(UpdateView):
    model = Producto
    template_name = 'producto.html'
    form_class = ProductoForm
    success_url = reverse_lazy('productos:listado_productos')

class ModificarCliente(UpdateView):
    model = cliente
    template_name = 'cliente.html'
    form_class = clienteForm
    success_url = reverse_lazy('productos:listado_clientes')

class ModificarProveedor(UpdateView):
    model = Proveedor
    template_name = 'proveedor.html'
    form_class = ProveedorForm
    success_url = reverse_lazy('productos:listado_proveedores')

class Modificarventa(UpdateView):
    model = venta
    template_name = 'venta.html'
    form_class = ventaForm
    success_url = reverse_lazy('productos:listado_ventas')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalles = Detalleventa.objects.filter(venta=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            d = {'producto': detalle.producto,
                 'cantidad': detalle.cantidad,
                 'precio_venta': detalle.precio_venta}
            detalles_data.append(d)
        detalle_venta_form_set = DetalleventaFormSet(initial=detalles_data)
        return self.render_to_response(self.get_context_data(form=form,
                                                             detalle_venta_form_set=detalle_venta_form_set))


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_venta_form_set = DetalleventaFormSet(request.POST)
        if form.is_valid() and detalle_venta_form_set.is_valid():
            return self.form_valid(form, detalle_venta_form_set)
        else:
            return self.form_invalid(form, detalle_venta_form_set)


    def form_valid(self, form, detalle_venta_form_set):
        self.object = form.save()
        detalle_venta_form_set.instance = self.object
        Detalleventa.objects.filter(venta = self.object).delete()
        detalle_venta_form_set.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, detalle_venta_form_set):
        return self.render_to_response(self.get_context_data(form=form,
                                                             detalle_venta_form_set = detalle_venta_form_set))

class DetalleProducto(DetailView):
    model = Producto
    template_name = 'detalle_producto.html'

class DetalleCliente(DetailView):
    model = cliente
    template_name = 'detalle_cliente.html'

class DetalleProveedor(DetailView):
    model = Proveedor
    template_name = 'detalle_proveedor.html'

class Crearventa(CreateView):
    model = venta
    template_name = 'venta.html'
    form_class = ventaForm
    success_url = reverse_lazy('productos:listado_ventas')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_orden_venta_formset=DetalleventaFormSet()
        return self.render_to_response(self.get_context_data(form=form,
                                                             detalle_venta_form_set=detalle_orden_venta_formset))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_venta_form_set = DetalleventaFormSet(request.POST)
        if form.is_valid() and detalle_venta_form_set.is_valid():
            return self.form_valid(form, detalle_venta_form_set)
        else:
            return self.form_invalid(form, detalle_venta_form_set)


    def form_valid(self, form, detalle_venta_form_set):
        self.object = form.save()
        detalle_venta_form_set.instance = self.object
        detalle_venta_form_set.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, detalle_venta_form_set):
        return self.render_to_response(self.get_context_data(form=form,
                                                             detalle_venta_form_set = detalle_venta_form_set))

#------------------------------------REPORTES------------------------------------------


#------------------------------------Modelo Cliente------------------------------------

class Reportes_de_ClientesPDF(View):


    def cabecera(self,pdf):
        
        archivo_imagen = settings.MEDIA_ROOT+'/imagenes/report-logo2.jpg'
        
        pdf.drawImage(archivo_imagen, 25, 720, 135, 90,preserveAspectRatio=True)

        pdf.setFont("Times-Roman", 25)
        
        pdf.drawString(195, 750,"LISTA DE CLIENTES")
        

    def tabla(self,pdf,y):
        encabezados = ('IDENTIFICACIÓN', 'NOMBRE','TELEFONO','DIRECCIÓN','E-MAIL')
        detalles = [(cliente.identificación, cliente.nombre  + cliente.apellido, cliente.telefono, cliente.dirección, cliente.correo_electronico) for cliente in cliente.objects.all()]
        List_clientes = Table([encabezados] + detalles, colWidths=[3 * cm, 5 * cm, 2.6 * cm, 4 * cm, 5 * cm])
        
        List_clientes.setStyle(TableStyle(
        [   
            ('BACKGROUND', (0, 0), (-1, 0), '#a7a5a5'),

            ('ALIGN',(0,0),(3,0),'CENTER'),
                
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            ('FONTSIZE', (0, 0), (-1, -1), 8.3),

            ]
        ))
        List_clientes.wrapOn(pdf, 800, 600)
        List_clientes.drawOn(pdf, 20,y+20)
        

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

#------------------------------------Modelo Productos-----------------------------------

class Reportes_de_ProductosPDF(View):

    def cabecera(self,pdf):
        
        archivo_imagen = settings.MEDIA_ROOT+'/imagenes/report-logo2.jpg'
        
        pdf.drawImage(archivo_imagen, 25, 720, 135, 90,preserveAspectRatio=True)

        pdf.setFont("Times-Roman", 25)
        
        pdf.drawString(195, 750,"LISTA DE PRODUCTOS")
        

    def tabla(self,pdf,y):
        encabezados = ('CODIGO', 'NOMBRE','STOCK','VALOR_UNITARIO','PROVEEDOR')
        detalles = [(Producto.codigo, Producto.nombre, Producto.stock, Producto.valor_unitario, Producto.proveedor) for Producto in Producto.objects.all()]
        List_productos = Table([encabezados] + detalles, colWidths=[3 * cm, 5 * cm, 2.6 * cm, 4 * cm, 5 * cm])
        
        List_productos.setStyle(TableStyle(
        [   
            ('BACKGROUND', (0, 0), (-1, 0), '#a7a5a5'),

            ('ALIGN',(0,0),(3,0),'CENTER'),
                
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            ('FONTSIZE', (0, 0), (-1, -1), 8.3),

            ]
        ))
        List_productos.wrapOn(pdf, 800, 600)
        List_productos.drawOn(pdf, 20,y+20)
        

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


#------------------------------------Modelo Proveedores------------------------------------

class Reportes_de_ProveedoresPDF(View):


    def cabecera(self,pdf):
        
        archivo_imagen = settings.MEDIA_ROOT+'/imagenes/report-logo2.jpg'
        
        pdf.drawImage(archivo_imagen, 25, 720, 135, 90,preserveAspectRatio=True)

        pdf.setFont("Times-Roman", 25)
        
        pdf.drawString(195, 750,"LISTA DE PROVEEDORES")
        

    def tabla(self,pdf,y):
        encabezados = ('RUC', 'RAZON_SOCIAL','DIRECCION','TELEFONO','E-MAIL','ESTADO')
        detalles = [(Proveedor.ruc, Proveedor.razon_social, Proveedor.direccion, Proveedor.telefono, Proveedor.correo, Proveedor.estado) for Proveedor in Proveedor.objects.all()]
        List_proveedores = Table([encabezados] + detalles, colWidths=[2.5 * cm, 4 * cm, 4 * cm, 2.6 * cm, 4.5 * cm, 2 *cm])
        
        List_proveedores.setStyle(TableStyle(
        [   
            ('BACKGROUND', (0, 0), (-1, 0), '#a7a5a5'),

            ('ALIGN',(0,0),(3,0),'CENTER'),
                
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            ('FONTSIZE', (0, 0), (-1, -1), 8.3),

            ]
        ))
        List_proveedores.wrapOn(pdf, 800, 600)
        List_proveedores.drawOn(pdf, 20,y+20)
        

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

