// Form validation script
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('acquisition-form');
    
    if (form) {
        // Add validation on form submission
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate numeric inputs (cantidad and precio_unitario)
            const numericInputs = form.querySelectorAll('input[name$="-cantidad"], input[name$="-precio_unitario"]');
            numericInputs.forEach(input => {
                // Check if the input is empty or not a positive number
                const value = parseFloat(input.value);
                if (isNaN(value) || value <= 0) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            // Validate product selections
            const productSelects = form.querySelectorAll('select[name$="-producto"]');
            productSelects.forEach(select => {
                if (!select.value) {
                    // If using Select2, we need to add the class to the Select2 container
                    if (typeof $.fn.select2 !== 'undefined') {
                        $(select).next('.select2-container').addClass('is-invalid');
                    } else {
                        select.classList.add('is-invalid');
                    }
                    isValid = false;
                } else {
                    if (typeof $.fn.select2 !== 'undefined') {
                        $(select).next('.select2-container').removeClass('is-invalid');
                    } else {
                        select.classList.remove('is-invalid');
                    }
                }
            });
            
            // Check if at least one product is added
            const formRows = form.querySelectorAll('#formset-container .form-row');
            if (formRows.length === 0) {
                alert('Debe agregar al menos un producto a la adquisición.');
                isValid = false;
            }
            
            // Validate the main form fields (proveedor and fecha)
            const proveedorSelect = form.querySelector('#id_proveedor');
            if (proveedorSelect && !proveedorSelect.value) {
                if (typeof $.fn.select2 !== 'undefined') {
                    $(proveedorSelect).next('.select2-container').addClass('is-invalid');
                } else {
                    proveedorSelect.classList.add('is-invalid');
                }
                isValid = false;
            }
            
            const fechaInput = form.querySelector('#id_fecha');
            if (fechaInput && !fechaInput.value) {
                fechaInput.classList.add('is-invalid');
                isValid = false;
            }
            
            // Prevent form submission if validation fails
            if (!isValid) {
                event.preventDefault();
                
                // Scroll to the first invalid element
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
        
        // Add real-time validation for numeric inputs
        form.addEventListener('input', function(event) {
            const target = event.target;
            
            // Only validate numeric inputs
            if (target.name && (target.name.includes('-cantidad') || target.name.includes('-precio_unitario'))) {
                const value = parseFloat(target.value);
                if (isNaN(value) || value <= 0) {
                    target.classList.add('is-invalid');
                } else {
                    target.classList.remove('is-invalid');
                }
            }
        });
    }
});