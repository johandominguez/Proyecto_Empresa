from django.urls   import path
from sistema.views import ListadoProductos, CrearProducto, ModificarProducto,DetalleProducto
from sistema.views import CrearProveedor, ListadoProveedores, ModificarProveedor, DetalleProveedor
from sistema.views import Crearventa, Modificarventa, Listadoventas 
from sistema.views import ListadoClientes, CrearCliente, ModificarCliente, DetalleCliente
from sistema.views import Reportes_de_ClientesPDF, Reportes_de_ProductosPDF, Reportes_de_ProveedoresPDF
from django.contrib.auth.decorators import login_required

prodcutos_patterns = ([

    path('', ListadoProductos.as_view(), name="listado_productos"),
    path('cliente/', ListadoClientes.as_view(), name="listado_clientes"),
    path('proveedores/', ListadoProveedores.as_view(), name="listado_proveedores"),
    path('crear_producto/', CrearProducto.as_view(), name="crear_producto"),
    path('modificar_producto/(?P<pk>.+)/',ModificarProducto.as_view(), name="modificar_producto"),
    path('detalle_producto/(?P<pk>.+)/',DetalleProducto.as_view(), name="detalle_producto"),
    path('crear_proveedor/', CrearProveedor.as_view(), name="crear_proveedor"),
    path('modificar_proveedor/(?P<pk>.+)/',ModificarProveedor.as_view(), name="modificar_proveedor"),
    path('detalle_proveedor/(?P<pk>.+)/',DetalleProveedor.as_view(), name="detalle_proveedor"),
    path('crear_cliente/', CrearCliente.as_view(), name="crear_cliente"),
    path('modificar_cliente/(?P<pk>.+)/',ModificarCliente.as_view(), name="modificar_cliente"),
    path('detalle_cliente/(?P<pk>.+)/',DetalleCliente.as_view(), name="detalle_cliente"),
    path('crear_venta/', Crearventa.as_view(), name="crear_venta"),
    path('modificar_venta/(?P<pk>.+)/',Modificarventa.as_view(), name="modificar_venta"),
    path('ventas/', Listadoventas.as_view(), name="listado_ventas"),
    path('reporte_clientespdf/',login_required(Reportes_de_ClientesPDF.as_view()), name="reporte_clientespdf"),
    path('reporte_productospdf/',login_required(Reportes_de_ProductosPDF.as_view()), name="reporte_productospdf"),
    path('reporte_proveedorespdf/',login_required(Reportes_de_ProveedoresPDF.as_view()), name="reporte_proveedorespdf"),
    
], 'productos')
