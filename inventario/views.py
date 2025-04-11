import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .models import (
    Categoria, Proveedor, Producto, 
    Adquisicion, DetalleAdquisicion, 
    Entrega, DetalleEntrega, Movimiento
)
from .forms import (
    CategoriaForm, ProveedorForm, ProductoForm, 
    AdquisicionForm, DetalleAdquisicionFormset,
    EntregaForm, DetalleEntregaFormset,
    AjusteStockForm, FechaRangoForm, ProductoFilterForm
)

# Vista Dashboard (versión segura)
@login_required
def dashboard(request):
    """
    Vista segura del dashboard que no accede a la base de datos
    para evitar errores durante migraciones o configuración inicial.
    """
    try:
        # Intentar obtener estadísticas básicas de forma segura
        from django.db import connection
        if connection.is_usable():
            total_productos = Producto.objects.count()
            stock_bajo = Producto.objects.filter(stock_actual__lt=F('stock_minimo')).count()
            sin_stock = Producto.objects.filter(stock_actual=0).count()
            adquisiciones_recientes = Adquisicion.objects.all().order_by('-fecha')[:5]
            entregas_recientes = Entrega.objects.all().order_by('-fecha')[:5]
            valor_total = Producto.objects.aggregate(
                total=Sum(F('stock_actual') * F('precio_costo'))
            )['total'] or 0
            
            context = {
                'total_productos': total_productos,
                'stock_bajo': stock_bajo,
                'sin_stock': sin_stock,
                'adquisiciones_recientes': adquisiciones_recientes,
                'entregas_recientes': entregas_recientes,
                'valor_total_inventario': valor_total,
                'db_ok': True
            }
        else:
            raise Exception("Database connection not usable")
    except Exception as e:
        # En caso de error, mostrar dashboard con datos vacíos
        context = {
            'total_productos': 0,
            'stock_bajo': 0,
            'sin_stock': 0,
            'adquisiciones_recientes': [],
            'entregas_recientes': [],
            'valor_total_inventario': 0,
            'db_ok': False,
            'error_message': str(e)
        }
    
    return render(request, 'inventario/dashboard.html', context)

# Vistas de Categorías
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'inventario/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inventario/categoria_form.html'
    success_url = reverse_lazy('categoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada correctamente.')
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inventario/categoria_form.html'
    success_url = reverse_lazy('categoria_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada correctamente.')
        return super().form_valid(form)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'inventario/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoría eliminada correctamente.')
        return super().delete(request, *args, **kwargs)

# Vistas de Proveedores
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'inventario/proveedor_list.html'
    context_object_name = 'proveedores'

class ProveedorDetailView(LoginRequiredMixin, DetailView):
    model = Proveedor
    template_name = 'inventario/proveedor_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adquisiciones'] = self.object.adquisiciones.all().order_by('-fecha')[:10]
        return context

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'inventario/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor creado correctamente.')
        return super().form_valid(form)

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'inventario/proveedor_form.html'
    success_url = reverse_lazy('proveedor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor actualizado correctamente.')
        return super().form_valid(form)

# Vistas de Productos
@login_required
def producto_list(request):
    form = ProductoFilterForm(request.GET or None)
    productos = Producto.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['nombre']:
            busqueda = form.cleaned_data['nombre']
            productos = productos.filter(
                Q(nombre__icontains=busqueda) | Q(codigo__icontains=busqueda)
            )
        
        if form.cleaned_data['categoria']:
            productos = productos.filter(categoria=form.cleaned_data['categoria'])
        
        if form.cleaned_data['stock_bajo']:
            productos = productos.filter(stock_actual__lt=F('stock_minimo'))
    
    return render(request, 'inventario/producto_list.html', {
        'productos': productos,
        'form': form
    })

class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'inventario/producto_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimientos'] = self.object.movimientos.all().order_by('-fecha')[:10]
        return context

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Registrar movimiento inicial si hay stock
        if form.instance.stock_actual > 0:
            Movimiento.objects.create(
                producto=form.instance,
                tipo='ajuste',
                cantidad=form.instance.stock_actual,
                stock_anterior=0,
                stock_nuevo=form.instance.stock_actual,
                descripcion='Stock inicial',
                usuario=self.request.user
            )
        
        messages.success(self.request, 'Producto creado correctamente.')
        return response

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_list')
    
    def form_valid(self, form):
        # Guardar stock anterior para registro de movimiento si cambia
        stock_anterior = self.get_object().stock_actual
        response = super().form_valid(form)
        
        # Si el stock cambió, registrar movimiento
        if stock_anterior != form.instance.stock_actual:
            Movimiento.objects.create(
                producto=form.instance,
                tipo='ajuste',
                cantidad=form.instance.stock_actual - stock_anterior,
                stock_anterior=stock_anterior,
                stock_nuevo=form.instance.stock_actual,
                descripcion='Ajuste desde edición de producto',
                usuario=self.request.user
            )
        
        messages.success(self.request, 'Producto actualizado correctamente.')
        return response

@login_required
def ajuste_stock(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = AjusteStockForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            motivo = form.cleaned_data['motivo']
            
            # Guardar el stock anterior
            stock_anterior = producto.stock_actual
            
            # Actualizar stock
            producto.stock_actual += cantidad
            if producto.stock_actual < 0:
                producto.stock_actual = 0
            producto.save()
            
            # Registrar movimiento
            Movimiento.objects.create(
                producto=producto,
                tipo='ajuste',
                cantidad=cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=producto.stock_actual,
                descripcion=motivo,
                usuario=request.user
            )
            
            messages.success(request, f'Stock ajustado correctamente. Nuevo stock: {producto.stock_actual}')
            return redirect('producto_detail', pk=producto.pk)
    else:
        form = AjusteStockForm()
    
    context = {
        'form': form,
        'producto': producto
    }
    return render(request, 'inventario/ajuste_stock.html', context)

# Vistas de Adquisiciones
class AdquisicionListView(LoginRequiredMixin, ListView):
    model = Adquisicion
    template_name = 'inventario/adquisicion_list.html'
    context_object_name = 'adquisiciones'
    ordering = ['-fecha']
    paginate_by = 10

class AdquisicionDetailView(LoginRequiredMixin, DetailView):
    model = Adquisicion
    template_name = 'inventario/adquisicion_detail.html'

@login_required
def adquisicion_create(request):
    if request.method == 'POST':
        form = AdquisicionForm(request.POST)
        if form.is_valid():
            adquisicion = form.save(commit=False)
            adquisicion.usuario = request.user
            adquisicion.save()
            
            formset = DetalleAdquisicionFormset(request.POST, instance=adquisicion)
            if formset.is_valid():
                formset.save()
                
                # Registrar movimientos para cada item
                for item in adquisicion.items.all():
                    # El stock ya se actualizó en el método save() de DetalleAdquisicion
                    # Solo necesitamos registrar el movimiento
                    Movimiento.objects.create(
                        producto=item.producto,
                        tipo='entrada',
                        cantidad=item.cantidad,
                        stock_anterior=item.producto.stock_actual - item.cantidad,
                        stock_nuevo=item.producto.stock_actual,
                        referencia=f'Adquisición #{adquisicion.id}',
                        usuario=request.user
                    )
                
                messages.success(request, 'Adquisición registrada correctamente.')
                return redirect('adquisicion_detail', pk=adquisicion.pk)
    else:
        form = AdquisicionForm()
        formset = DetalleAdquisicionFormset()
    
    return render(request, 'inventario/adquisicion_form.html', {
        'form': form,
        'formset': formset
    })

# Vistas de Entregas
class EntregaListView(LoginRequiredMixin, ListView):
    model = Entrega
    template_name = 'inventario/entrega_list.html'
    context_object_name = 'entregas'
    ordering = ['-fecha']
    paginate_by = 10

class EntregaDetailView(LoginRequiredMixin, DetailView):
    model = Entrega
    template_name = 'inventario/entrega_detail.html'

@login_required
def entrega_create(request):
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.usuario = request.user
            entrega.save()
            
            formset = DetalleEntregaFormset(request.POST, instance=entrega)
            if formset.is_valid():
                # Verificar stock disponible antes de guardar
                error = False
                for form in formset:
                    if form.is_valid() and not form.cleaned_data.get('DELETE', False):
                        producto = form.cleaned_data.get('producto')
                        cantidad = form.cleaned_data.get('cantidad')
                        if producto and cantidad:
                            if producto.stock_actual < cantidad:
                                messages.error(request, f'Stock insuficiente para {producto}. Disponible: {producto.stock_actual}')
                                error = True
                
                if error:
                    # Si hay error, eliminar la entrega creada y volver al formulario
                    entrega.delete()
                    return render(request, 'inventario/entrega_form.html', {
                        'form': form,
                        'formset': formset
                    })
                
                formset.save()
                
                # Registrar movimientos para cada item
                for item in entrega.items.all():
                    # El stock ya se actualizó en el método save() de DetalleEntrega
                    # Solo necesitamos registrar el movimiento
                    Movimiento.objects.create(
                        producto=item.producto,
                        tipo='salida',
                        cantidad=-item.cantidad,  # Negativo para indicar salida
                        stock_anterior=item.producto.stock_actual + item.cantidad,
                        stock_nuevo=item.producto.stock_actual,
                        referencia=f'Entrega #{entrega.id}',
                        usuario=request.user
                    )
                
                messages.success(request, 'Entrega registrada correctamente.')
                return redirect('entrega_detail', pk=entrega.pk)
    else:
        form = EntregaForm()
        formset = DetalleEntregaFormset()
    
    return render(request, 'inventario/entrega_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
def entrega_cambiar_estado(request, pk, estado):
    entrega = get_object_or_404(Entrega, pk=pk)
    estado_anterior = entrega.estado
    
    if estado in ['pendiente', 'entregado', 'cancelado']:
        entrega.estado = estado
        entrega.save()
        
        # Si se cancela una entrega, devolver productos al stock
        if estado == 'cancelado' and estado_anterior != 'cancelado':
            for item in entrega.items.all():
                # Guardar stock anterior
                stock_anterior = item.producto.stock_actual
                
                # Devolver al stock
                item.producto.stock_actual += item.cantidad
                item.producto.save()
                
                # Registrar movimiento
                Movimiento.objects.create(
                    producto=item.producto,
                    tipo='ajuste',
                    cantidad=item.cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=item.producto.stock_actual,
                    referencia=f'Cancelación entrega #{entrega.id}',
                    usuario=request.user
                )
        
        # Si se reactiva una entrega cancelada, volver a descontar
        elif estado != 'cancelado' and estado_anterior == 'cancelado':
            for item in entrega.items.all():
                # Guardar stock anterior
                stock_anterior = item.producto.stock_actual
                
                # Restar del stock
                item.producto.stock_actual -= item.cantidad
                if item.producto.stock_actual < 0:
                    item.producto.stock_actual = 0
                item.producto.save()
                
                # Registrar movimiento
                Movimiento.objects.create(
                    producto=item.producto,
                    tipo='ajuste',
                    cantidad=-item.cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=item.producto.stock_actual,
                    referencia=f'Reactivación entrega #{entrega.id}',
                    usuario=request.user
                )
        
        messages.success(request, f'Estado de entrega actualizado a: {estado}')
    else:
        messages.error(request, 'Estado no válido')
    
    return redirect('entrega_detail', pk=entrega.pk)

# Vistas de Reportes
@login_required
def reporte_movimientos(request):
    form = FechaRangoForm(request.GET or None)
    movimientos = None
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        
        # Ajustar fecha_fin para incluir todo el día
        fecha_fin = datetime.combine(fecha_fin, datetime.time.max)
        
        movimientos = Movimiento.objects.filter(
            fecha__range=(fecha_inicio, fecha_fin)
        ).order_by('-fecha')
    
    return render(request, 'inventario/reporte_movimientos.html', {
        'form': form,
        'movimientos': movimientos
    })

@login_required
def reporte_stock(request):
    form = ProductoFilterForm(request.GET or None)
    productos = Producto.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['nombre']:
            busqueda = form.cleaned_data['nombre']
            productos = productos.filter(
                Q(nombre__icontains=busqueda) | Q(codigo__icontains=busqueda)
            )
        
        if form.cleaned_data['categoria']:
            productos = productos.filter(categoria=form.cleaned_data['categoria'])
        
        if form.cleaned_data['stock_bajo']:
            productos = productos.filter(stock_actual__lt=F('stock_minimo'))
    
    # Calcular valor total del inventario
    valor_total = productos.aggregate(
        total=Sum(F('stock_actual') * F('precio_costo'))
    )['total'] or 0
    
    return render(request, 'inventario/reporte_stock.html', {
        'form': form,
        'productos': productos,
        'valor_total': valor_total
    })
