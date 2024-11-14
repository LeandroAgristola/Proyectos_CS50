document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  load_mailbox('inbox');
});

function compose_email() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({ recipients, subject, body }),
      headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(result => {
      if (result.message === "Email sent successfully.") {
        alert("Email enviado con éxito.");
        load_mailbox('sent');
      } else {
        alert("Error al enviar el email: " + result.error);
      }
    })
    .catch(error => console.error("Error:", error));
  };
}

function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <div id="emails-list"></div>
  `;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      const emailsList = document.querySelector('#emails-list');
      emailsList.innerHTML = '';

      emails.forEach(email => {
        const emailItem = document.createElement('div');
        emailItem.className = 'email-item';

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
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';

  // Fetch email details
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Marcar como leído
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({ read: true }),
          headers: { "Content-Type": "application/json" }
        });
      }

      // Renderizar el contenido del email
      document.querySelector('#email-detail-view').innerHTML = `
        <h3>${email.subject}</h3>
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body}</p>
      `;

      // Agregar botones de archivar y responder
      if (!email.sent) {
        const archiveButton = document.createElement('button');
        archiveButton.className = 'btn btn-secondary';
        archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
        archiveButton.addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({ archived: !email.archived }),
            headers: { "Content-Type": "application/json" }
          })
          .then(() => load_mailbox('inbox'));
        });
        document.querySelector('#email-detail-view').appendChild(archiveButton);
      }

      const replyButton = document.createElement('button');
      replyButton.className = 'btn btn-primary ml-2';
      replyButton.innerHTML = 'Reply';
      replyButton.addEventListener('click', () => {
        compose_email();
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
      });

      const deleteButton = document.createElement('button');
      deleteButton.className = 'btn btn-danger ml-2';
      deleteButton.innerHTML = 'Delete';
      deleteButton.addEventListener('click', () => {
        fetch(`/emails/${email_id}`, {
          method: 'DELETE',
          headers: { "Content-Type": "application/json" }
        })
        .then(() => load_mailbox('inbox'));
      });

      document.querySelector('#email-detail-view').append(replyButton, deleteButton);
    })
    .catch(error => console.error('Error:', error));
}