// Inicialización de tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Auto-cerrar alertas después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-danger)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Manejar formsets dinámicos para adquisiciones y entregas
    if (document.querySelector('.formset-container')) {
        setupFormsets();
    }
});

// Función para manejar formsets dinámicos
function setupFormsets() {
    // Seleccionar el contenedor del formset y el botón para agregar
    const formsetContainer = document.querySelector('.formset-container');
    const addButton = document.querySelector('.add-form-row');
    
    if (!formsetContainer || !addButton) return;
    
    // Evento para agregar una nueva fila
    addButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Obtener el total de formularios actual
        const totalForms = document.querySelector('#id_items-TOTAL_FORMS');
        const currentFormCount = parseInt(totalForms.value);
        
        // Obtener la primera fila (template)
        const formRow = formsetContainer.querySelector('.form-row:first-child').cloneNode(true);
        
        // Actualizar IDs y atributos name
        updateFormRow(formRow, currentFormCount);
        
        // Limpiar valores
        formRow.querySelectorAll('input, select').forEach(input => {
            if (input.type === 'checkbox') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });
        
        // Agregar la nueva fila
        formsetContainer.appendChild(formRow);
        
        // Actualizar el contador de formularios
        totalForms.value = currentFormCount + 1;
    });
    
    // Delegación de eventos para eliminar filas
    formsetContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-form-row')) {
            e.preventDefault();
            
            const formRow = e.target.closest('.form-row');
            const deleteCheckbox = formRow.querySelector('input[name$="-DELETE"]');
            
            if (deleteCheckbox) {
                // Si hay un checkbox DELETE, marcarlo (para formsets existentes)
                deleteCheckbox.checked = true;
                formRow.style.display = 'none';
            } else {
                // Si no hay checkbox DELETE, remover la fila (para formsets nuevos)
                formRow.remove();
                
                // Actualizar el contador de formularios
                const totalForms = document.querySelector('#id_items-TOTAL_FORMS');
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        }
    });
}

// Función para actualizar IDs y atributos name en una fila de formset
function updateFormRow(row, index) {
    // Actualizar IDs y atributos name con el nuevo índice
    row.querySelectorAll('input, select, label').forEach(element => {
        if (element.id) {
            element.id = element.id.replace(/-\d+-/, `-${index}-`);
        }
        if (element.name) {
            element.name = element.name.replace(/-\d+-/, `-${index}-`);
        }
        if (element.htmlFor) {
            element.htmlFor = element.htmlFor.replace(/-\d+-/, `-${index}-`);
        }
    });
    
    return row;
}