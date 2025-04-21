$(document).ready(function () {
    const addFormButton = $('#add-form-button');
    const formsetContainer = $('#formset-container');
    const emptyFormTemplate = $('#empty-form').html();
    const totalForms = $('#id_form-TOTAL_FORMS');
    const formPrefix = 'form';

    function updateSubtotal(row) {
        const cantidadInput = row.find('[id$="-cantidad"]');
        const precioInput = row.find('[id$="-precio_unitario"]');
        const subtotalCell = row.find('[class^="subtotal-"]');

        if (cantidadInput.length && precioInput.length && subtotalCell.length) {
            const cantidad = parseFloat(cantidadInput.val()) || 0;
            const precio = parseFloat(precioInput.val()) || 0;
            const subtotal = cantidad * precio;
            subtotalCell.text(subtotal.toFixed(2));
        }
    }

    function updateTotal() {
        let total = 0;
        formsetContainer.find('tr:visible').each(function() {
            const subtotalCell = $(this).find('[class^="subtotal-"]');
            if (subtotalCell.length) {
                total += parseFloat(subtotalCell.text()) || 0;
            }
        });
        $('#total-amount').text(total.toFixed(2));
    }

    function addNewForm() {
        const newFormIndex = totalForms.val();
        // Reemplazo correctamente los prefijos en el template
        let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, newFormIndex).replace(/-empty-/g, `-${newFormIndex}-`);
        // Si el template ya es un <tr>, lo convierto a jQuery object
        let newRow = $(newFormHtml);
        // Si no es <tr> (por si acaso), lo envuelvo
        if (!newRow.is('tr')) {
            newRow = $('<tr class="form-row">').append(newFormHtml);
        }
        // Ajusto el id del checkbox de borrado si existe
        const deleteCheckbox = newRow.find('[id$="-DELETE"]');
        if (deleteCheckbox.length) {
            const newId = `id_form-${newFormIndex}-DELETE`;
            deleteCheckbox.attr('id', newId);
        }
        formsetContainer.append(newRow);
        totalForms.val(parseInt(totalForms.val()) + 1);
        // Inicializar Select2 si corresponde
        newRow.find('select').each(function() {
            if (typeof $.fn.select2 !== 'undefined') {
                $(this).select2({
                    theme: 'bootstrap4',
                    width: '100%'
                });
            }
        });
        updateTotal();
    }

    addFormButton.on('click', addNewForm);

    formsetContainer.on('click', '.delete-form-button', function () {
        const button = $(this);
        const row = button.closest('tr');
        const deleteCheckbox = row.find('[id$="-DELETE"]');

        if (deleteCheckbox.length) {
            deleteCheckbox.prop('checked', true);
            row.hide();
        } else {
            row.remove();
            totalForms.val(parseInt(totalForms.val()) - 1);
        }
        updateTotal();
    });

    formsetContainer.on('change', '[id$="-cantidad"], [id$="-precio_unitario"]', function () {
        const input = $(this);
        const row = input.closest('tr');
        updateSubtotal(row);
        updateTotal();
    });

    // Inicialización
    formsetContainer.find('tr').each(function() {
        updateSubtotal($(this));
    });
    updateTotal();
});