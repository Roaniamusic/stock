# Generated by Django 4.2.7 on 2025-04-11 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adquisicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_factura', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Adquisición',
                'verbose_name_plural': 'Adquisiciones',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('contacto', models.CharField(blank=True, max_length=200, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('rut', models.CharField(blank=True, max_length=20, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio_costo', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('precio_venta', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('stock_actual', models.PositiveIntegerField(default=0)),
                ('stock_minimo', models.PositiveIntegerField(default=5)),
                ('ubicacion', models.CharField(blank=True, max_length=100, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('ultima_actualizacion', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='inventario.categoria')),
                ('proveedor_principal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='inventario.proveedor')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida'), ('ajuste', 'Ajuste')], max_length=20)),
                ('cantidad', models.IntegerField()),
                ('stock_anterior', models.PositiveIntegerField()),
                ('stock_nuevo', models.PositiveIntegerField()),
                ('referencia', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='inventario.producto')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Movimiento',
                'verbose_name_plural': 'Movimientos',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destinatario', models.CharField(max_length=200)),
                ('departamento', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('entregado', 'Entregado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entrega',
                'verbose_name_plural': 'Entregas',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='DetalleEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventario.entrega')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
            ],
            options={
                'verbose_name': 'Detalle de entrega',
                'verbose_name_plural': 'Detalles de entregas',
            },
        ),
        migrations.CreateModel(
            name='DetalleAdquisicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('adquisicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventario.adquisicion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
            ],
            options={
                'verbose_name': 'Detalle de adquisición',
                'verbose_name_plural': 'Detalles de adquisiciones',
            },
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adquisiciones', to='inventario.proveedor'),
        ),
        migrations.AddField(
            model_name='adquisicion',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
