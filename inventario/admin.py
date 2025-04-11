from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Categoria, Proveedor, Producto, 
    Adquisicion, DetalleAdquisicion, 
    Entrega, DetalleEntrega, Movimiento
)

class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')

class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'email', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'contacto', 'email', 'rut')

class ProductoAdmin(ImportExportModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'stock_actual', 'stock_minimo', 'estado_stock', 'precio_costo', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('codigo', 'nombre', 'descripcion')
    readonly_fields = ('stock_actual', 'fecha_creacion', 'ultima_actualizacion')
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'categoria', 'imagen', 'activo')
        }),
        ('Proveedor y Precios', {
            'fields': ('proveedor_principal', 'precio_costo', 'precio_venta')
        }),
        ('Inventario', {
            'fields': ('stock_actual', 'stock_minimo', 'ubicacion')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class DetalleAdquisicionInline(admin.TabularInline):
    model = DetalleAdquisicion
    extra = 1
    autocomplete_fields = ['producto']

class AdquisicionAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha', 'total', 'usuario')
    list_filter = ('proveedor', 'fecha')
    search_fields = ('proveedor__nombre', 'numero_factura')
    inlines = [DetalleAdquisicionInline]
    readonly_fields = ('total', 'usuario', 'fecha_registro')

class DetalleEntregaInline(admin.TabularInline):
    model = DetalleEntrega
    extra = 1
    autocomplete_fields = ['producto']

class EntregaAdmin(admin.ModelAdmin):
    list_display = ('id', 'destinatario', 'departamento', 'fecha', 'estado', 'usuario')
    list_filter = ('estado', 'fecha', 'departamento')
    search_fields = ('destinatario', 'departamento')
    inlines = [DetalleEntregaInline]
    readonly_fields = ('usuario', 'fecha_registro')

class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'tipo', 'cantidad', 'stock_anterior', 'stock_nuevo', 'usuario', 'fecha')
    list_filter = ('tipo', 'fecha', 'usuario')
    search_fields = ('producto__nombre', 'producto__codigo', 'descripcion')
    readonly_fields = ('producto', 'tipo', 'cantidad', 'stock_anterior', 'stock_nuevo', 'referencia', 'descripcion', 'usuario', 'fecha')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Adquisicion, AdquisicionAdmin)
admin.site.register(Entrega, EntregaAdmin)
admin.site.register(Movimiento, MovimientoAdmin)