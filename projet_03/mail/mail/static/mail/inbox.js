document.addEventListener('DOMContentLoaded', function() {

  // Configurar eventos para las vistas
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Cargar la bandeja de entrada por defecto
  load_mailbox('inbox');
});

function compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Limpiar campos
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Enviar formulario
  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Realizar POST
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(response => response.json())
    .then(result => {
      if (result.message === "Email sent successfully.") {
        // Notificación de éxito y redirigir a "Sent"
        alert("Email enviado con éxito.");
        load_mailbox('sent');
      } else {
        // Notificación de error
        alert("Error al enviar el email: " + result.error);
      }
    })
    .catch(error => console.error("Error:", error));
  };
}

function load_mailbox(mailbox) {
  // Mostrar la vista de correos y ocultar la vista de composición
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Configurar el título de la vista
  document.querySelector('#emails-view').innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <div id="emails-list"></div> <!-- Asegura que el contenedor emails-list esté presente -->
  `;

  // Realizar la solicitud GET a la bandeja correspondiente
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      const emailsList = document.querySelector('#emails-list'); // Seleccionar emails-list
      emailsList.innerHTML = ''; // Limpiar lista

      emails.forEach(email => {
        // Crear el elemento HTML para cada correo
        const emailItem = document.createElement('div');
        emailItem.className = 'email-item';

        // Si el correo está leído, agregar la clase 'read', si no, 'unread'
        if (email.read) {
          emailItem.classList.add('read');
        } else {
          emailItem.classList.add('unread');
        }

        emailItem.innerHTML = `
          <strong>${email.sender}</strong> - ${email.subject} 
          <span class="timestamp">${email.timestamp}</span>
        `;

        emailItem.addEventListener('click', () => view_email(email.id));
        emailsList.append(emailItem);
      });
    })
    .catch(error => console.error('Error:', error));
}

function view_email(email_id) {
  // Hide other views and show the email detail view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  // Fetch the email details
  fetch(`/emails/${email_id}`)
      .then(response => response.json())
      .then(email => {
          // Display email contents
          document.querySelector('#email-detail-view').innerHTML = `
              <h3>${email.subject}</h3>
              <p><strong>From:</strong> ${email.sender}</p>
              <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
              <p><strong>Timestamp:</strong> ${email.timestamp}</p>
              <hr>
              <p>${email.body}</p>
          `;

          // Mark email as read
          if (!email.read) {
              fetch(`/emails/${email_id}`, {
                  method: 'PUT',
                  body: JSON.stringify({ read: true }),
                  headers: { "Content-Type": "application/json" }
              });
          }
      })
      .catch(error => console.error('Error:', error));
}