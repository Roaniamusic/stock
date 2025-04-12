"""
Script para probar la generación de PDF independientemente del resto de la aplicación.
Ejecutar desde la línea de comandos: python test_pdf.py
"""
import os
import sys
import django

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockeando.settings')
django.setup()

from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from inventario.models import Entrega
from django.contrib.auth.models import User

def generar_pdf_prueba(entrega_id):
    """Genera un PDF de prueba para una entrega específica"""
    try:
        # Obtener la entrega
        entrega = Entrega.objects.get(pk=entrega_id)
        
        # Obtener un usuario cualquiera para pruebas
        usuario = User.objects.first()
        
        # Obtener el template HTML
        template = get_template('inventario/remito_pdf.html')
        
        # Preparar el contexto para el template
        context = {
            'entrega': entrega,
            'items': entrega.items.all(),
            'fecha_impresion': datetime.now(),
            'usuario': usuario,
            'empresa': {
                'nombre': 'Mi Empresa S.A.',
                'direccion': 'Calle Principal 123, Ciudad',
                'telefono': '(123) 456-7890',
                'email': 'contacto@miempresa.com',
            }
        }
        
        # Renderizar HTML
        html = template.render(context)
        
        # Nombre del archivo de salida
        output_filename = f"remito_entrega_{entrega_id}_test.pdf"
        
        # Generar el PDF
        with open(output_filename, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            
        # Verificar el resultado
        if pisa_status.err:
            print(f"Error al generar PDF: {pisa_status.err}")
            return False
        else:
            print(f"PDF generado exitosamente: {output_filename}")
            return True
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        entrega_id = int(sys.argv[1])
        generar_pdf_prueba(entrega_id)
    else:
        print("Uso: python test_pdf.py [ID_ENTREGA]")