from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/eliminar/<int:pk>/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    
    # Proveedores
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/<int:pk>/', views.ProveedorDetailView.as_view(), name='proveedor_detail'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', views.ProveedorUpdateView.as_view(), name='proveedor_update'),
    
    # Productos
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/ajuste/', views.ajuste_stock, name='ajuste_stock'),
    
    # Adquisiciones
    path('adquisiciones/', views.AdquisicionListView.as_view(), name='adquisicion_list'),
    path('adquisiciones/<int:pk>/', views.AdquisicionDetailView.as_view(), name='adquisicion_detail'),
    path('adquisiciones/nueva/', views.adquisicion_create, name='adquisicion_create'),
    path('adquisiciones/editar/<int:pk>/', views.AdquisicionUpdateView.as_view(), name='adquisicion_edit'),
    path('adquisiciones/eliminar/<int:pk>/', views.AdquisicionDeleteView.as_view(), name='adquisicion_delete'),
    
    # Entregas
    path('entregas/', views.EntregaListView.as_view(), name='entrega_list'),
    path('entregas/<int:pk>/', views.EntregaDetailView.as_view(), name='entrega_detail'),
    path('entregas/nueva/', views.entrega_create, name='entrega_create'),
    path('entregas/editar/<int:pk>/', views.EntregaUpdateView.as_view(), name='entrega_edit'),
    path('entregas/eliminar/<int:pk>/', views.EntregaDeleteView.as_view(), name='entrega_delete'),
    path('entregas/<int:pk>/estado/<str:estado>/', views.entrega_cambiar_estado, name='entrega_cambiar_estado'),
    path('entregas/<int:pk>/remito/', views.generar_remito_pdf, name='entrega_remito'),
    
    # Reportes
    path('reportes/movimientos/', views.reporte_movimientos, name='reporte_movimientos'),
    path('reportes/stock/', views.reporte_stock, name='reporte_stock'),
]
