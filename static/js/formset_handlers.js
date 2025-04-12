// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Select2 if it's being used
    if (typeof $.fn.select2 !== 'undefined') {
        $('select').select2({
            theme: 'bootstrap4',
            width: '100%'
        });
    }

    // Set up the form prefix (adjust if your formset has a different prefix)
    const prefix = 'form';
    const formsetContainer = document.getElementById('formset-container');
    
    // Get the total number of forms from the management form
    let totalForms = document.querySelector('#id_' + prefix + '-TOTAL_FORMS');
    
    // Add form button functionality
    document.getElementById('add-form-button').addEventListener('click', function() {
        addForm(prefix, formsetContainer, totalForms);
    });
    
    // Initial calculation of all subtotals
    calculateAllSubtotals();
    
    // Add event listeners for quantity and price changes
    document.addEventListener('change', function(e) {
        if (e.target.name && (e.target.name.includes('-cantidad') || e.target.name.includes('-precio_unitario'))) {
            calculateAllSubtotals();
        }
    });
    
    // Add event delegation for delete buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-form-button') || 
            e.target.closest('.delete-form-button')) {
            
            if (confirm('¿Está seguro que desea eliminar este producto?')) {
                const formRow = e.target.closest('.form-row');
                if (formRow) {
                    // If there's only one form, just clear it instead of removing
                    if (parseInt(totalForms.value) > 1) {
                        formRow.remove();
                        updateFormIndexes(prefix);
                        totalForms.value = parseInt(totalForms.value) - 1;
                    } else {
                        // Clear inputs instead of removing the only form
                        const inputs = formRow.querySelectorAll('input:not([type=hidden]), select');
                        inputs.forEach(input => {
                            if (input.tagName === 'SELECT') {
                                input.selectedIndex = 0;
                                if (typeof $.fn.select2 !== 'undefined') {
                                    $(input).trigger('change');
                                }
                            } else {
                                input.value = '';
                            }
                        });
                    }
                    calculateAllSubtotals();
                }
            }
            
            e.preventDefault();
        }
    });
});

// Function to add a new form to the formset
function addForm(prefix, container, totalForms) {
    // Get the template form (usually the first one)
    const formRegex = new RegExp(prefix + '-(\\d+)-', 'g');
    const formIndex = parseInt(totalForms.value);
    
    // Clone the first form
    const firstForm = container.querySelector('.form-row');
    const newForm = firstForm.cloneNode(true);
    
    // Update form index
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, prefix + '-' + formIndex + '-');
    
    // Clear input values in the new form
    const inputs = newForm.querySelectorAll('input:not([type=hidden]), select');
    inputs.forEach(input => {
        if (input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        } else {
            input.value = '';
        }
    });
    
    // Update subtotal cell ID
    const subtotalCell = newForm.querySelector('[class^="subtotal-"]');
    if (subtotalCell) {
        subtotalCell.className = 'subtotal-' + formIndex;
        subtotalCell.textContent = '0.00';
    }
    
    // Append the new form
    container.appendChild(newForm);
    
    // Initialize Select2 on new selects if needed
    if (typeof $.fn.select2 !== 'undefined') {
        $(newForm).find('select').select2({
            theme: 'bootstrap4',
            width: '100%'
        });
    }
    
    // Update total forms count
    totalForms.value = formIndex + 1;
}

// Function to update form indexes after deletion
function updateFormIndexes(prefix) {
    const container = document.getElementById('formset-container');
    const forms = container.querySelectorAll('.form-row');
    const totalForms = document.querySelector('#id_' + prefix + '-TOTAL_FORMS');
    
    forms.forEach((form, index) => {
        const formRegex = new RegExp(prefix + '-(\\d+)-', 'g');
        form.innerHTML = form.innerHTML.replace(formRegex, prefix + '-' + index + '-');
        
        // Update subtotal cell class
        const subtotalCell = form.querySelector('[class^="subtotal-"]');
        if (subtotalCell) {
            subtotalCell.className = 'subtotal-' + index;
        }
    });
    
    totalForms.value = forms.length;
}

// Function to calculate all subtotals and update total
function calculateAllSubtotals() {
    let total = 0;
    const rows = document.querySelectorAll('#formset-container .form-row');
    
    rows.forEach((row, index) => {
        const cantidadInput = row.querySelector('input[name$="-cantidad"]');
        const precioInput = row.querySelector('input[name$="-precio_unitario"]');
        
        if (cantidadInput && precioInput) {
            const cantidad = parseFloat(cantidadInput.value) || 0;
            const precio = parseFloat(precioInput.value) || 0;
            const subtotal = cantidad * precio;
            
            // Update subtotal cell
            const subtotalCell = document.querySelector('.subtotal-' + index);
            if (subtotalCell) {
                subtotalCell.textContent = formatCurrency(subtotal);
            }
            
            total += subtotal;
        }
    });
    
    // Update total amount
    const totalElement = document.getElementById('total-amount');
    if (totalElement) {
        totalElement.textContent = formatCurrency(total);
    }
}

// Helper function to format currency
function formatCurrency(value) {
    return value.toLocaleString('es-ES', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}