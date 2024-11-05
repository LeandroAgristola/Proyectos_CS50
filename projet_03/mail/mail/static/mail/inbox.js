document.addEventListener('DOMContentLoaded', function() {
  // Navegación entre vistas
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Cargar por defecto la bandeja de entrada
  load_mailbox('inbox');
});

// Función para mostrar la vista de redacción
function compose_email() {
  // Mostrar la vista de redacción y ocultar las demás
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Limpiar campos de redacción
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Función para cargar la vista de la bandeja de entrada
function load_mailbox(mailbox) {
  // Mostrar la bandeja de entrada y ocultar la vista de redacción
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Mostrar el nombre de la bandeja de entrada
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Realizar una solicitud GET para obtener los correos de la bandeja
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Limpiar la vista antes de mostrar los correos
      document.querySelector('#emails-view').innerHTML = '';

      // Iterar sobre cada correo y crear un elemento HTML para mostrarlo
      emails.forEach(email => {
          const email_div = document.createElement('div');
          email_div.innerHTML = `
              <strong>De:</strong> ${email.sender} <br>
              <strong>Asunto:</strong> ${email.subject} <br>
              <strong>Fecha:</strong> ${email.timestamp} <br>
          `;
          email_div.classList.add('email-item');
          document.querySelector('#emails-view').append(email_div);
      });
  });
}
