# Stockeando - Sistema de Control de Stock

Sistema desarrollado con Django para gestionar inventario, adquisiciones y entregas de productos.

## Requisitos

- Python 3.8+
- Django 4.2+
- Otras dependencias en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-repositorio>
cd stockeando
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

## Características

- Gestión de productos e inventario
- Registro de proveedores
- Adquisiciones (entrada de stock)
- Entregas (salida de stock)
- Reportes básicos
- Autenticación de usuarios#   s t o c k  
 