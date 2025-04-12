from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    proveedor_principal = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def get_absolute_url(self):
        return reverse('producto_detalle', kwargs={'pk': self.pk})
    
    @property
    def valor_inventario(self):
        return self.precio_costo * self.stock_actual
    
    @property
    def estado_stock(self):
        if self.stock_actual <= 0:
            return "Sin stock"
        elif self.stock_actual < self.stock_minimo:
            return "Stock bajo"
        else:
            return "Stock normal"

class Adquisicion(models.Model):
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='adquisiciones')
    fecha = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Adquisición'
        verbose_name_plural = 'Adquisiciones'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Adquisición #{self.id} - {self.proveedor}"
    
    def actualizar_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total = total
        self.save()
    
    @property
    def total_calculado(self):
        """Calcula el total de toda la adquisición"""
        return sum(item.subtotal for item in self.items.all())

class DetalleAdquisicion(models.Model):
    adquisicion = models.ForeignKey(Adquisicion, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de adquisición'
        verbose_name_plural = 'Detalles de adquisiciones'
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal para este ítem de adquisición"""
        return self.cantidad * self.precio_unitario
    
    def save(self, *args, **kwargs):
        # Actualizar stock del producto al guardar
        self.producto.stock_actual += self.cantidad
        self.producto.save()
        super().save(*args, **kwargs)
        # Actualizar total de la adquisición
        self.adquisicion.actualizar_total()

class Entrega(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    
    destinatario = models.CharField(max_length=200)
    departamento = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Entrega #{self.id} - {self.destinatario}"
    
    @property
    def total(self):
        """Calcula el total de toda la entrega"""
        return sum(item.subtotal for item in self.items.all())

class DetalleEntrega(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Detalle de entrega'
        verbose_name_plural = 'Detalles de entregas'
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal para este ítem de entrega"""
        return self.cantidad * self.producto.precio_venta
    
    def save(self, *args, **kwargs):
        # Actualizar stock del producto al guardar
        if self.entrega.estado != 'cancelado':
            self.producto.stock_actual -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)

class Movimiento(models.Model):
    TIPOS = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    )
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    cantidad = models.IntegerField()  # Puede ser negativo para salidas
    stock_anterior = models.PositiveIntegerField()
    stock_nuevo = models.PositiveIntegerField()
    referencia = models.CharField(max_length=100, blank=True, null=True)  # Para almacenar referencia a adquisición o entrega
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.producto} ({self.cantidad})"
