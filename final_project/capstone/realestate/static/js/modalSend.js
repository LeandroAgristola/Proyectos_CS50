document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form-contacto');
    var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    var mensajeModal = new bootstrap.Modal(document.getElementById('mensajeModal'));

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            var formData = new FormData(form);

            document.querySelectorAll('.alert.alert-danger').forEach(function(element) {
                element.remove();
            });

            loadingModal.show();

            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                loadingModal.hide();

                if (data.status === 'ok' || data.status === 'simulated') {
                    mensajeModal.show();
                    form.reset();
                } else if (data.status === 'invalid') {
                    console.log('Errores de validación:', data.errors);

                    var errors = JSON.parse(data.errors);
                    for (var field in errors) {
                        var errorMessages = errors[field];
                        var fieldElement = document.querySelector('[name=' + field + ']');
                        if (fieldElement) {
                            var errorElement = document.createElement('div');
                            errorElement.className = 'alert alert-danger';
                            errorMessages.forEach(function(error) {
                                var errorText = document.createTextNode(error.message);
                                errorElement.appendChild(errorText);
                            });
                            fieldElement.parentElement.appendChild(errorElement);
                        }
                    }
                }
            })
            .catch(error => {
                loadingModal.hide();
                console.error('Error al enviar el formulario:', error);
                alert('Hubo un problema al enviar el formulario. Por favor, inténtalo nuevamente.');
            });
        });
    }
});