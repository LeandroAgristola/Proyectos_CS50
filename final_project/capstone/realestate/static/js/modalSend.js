document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('contactForm');
    var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    var msjModal = new bootstrap.Modal(document.getElementById('msjModal'));

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); 

            var formData = new FormData(form);

            document.querySelectorAll('.alert.alert-danger').forEach(function(element) {
                element.remove();
            });

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
                if (data.status === 'ok') {
                    loadingModal.show();
                    setTimeout(() => {
                        loadingModal.hide();
                        msjModal.show();
                        form.reset();
                    }, 1000);
                } else if (data.status === 'invalid') {
                    console.log('Validation errors:', data.errors);
                    
                    var errors = JSON.parse(data.errors);
                    for (var field in errors) {
                        var errorMessages = errors[field];
                        var fieldElement = document.querySelector('[name=' + field + ']');
                        if (fieldElement) {
                            var errorElement = document.createElement('div');
                            errorElement.className = 'alert alert-danger mt-2';
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
                console.error('Error sending form:', error);
            });
        });
    }
});
