document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails for the specified mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Clear out any existing content in the emails view
      document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
      
      // Iterate through each email and create a display for it
      emails.forEach(email => {
        const email_div = document.createElement('div');
        email_div.classList.add('email-item');

        // Add email details to the div
        email_div.innerHTML = `
          <div><strong>De:</strong> ${email.sender}</div>
          <div><strong>Asunto:</strong> ${email.subject}</div>
          <div><strong>Fecha:</strong> ${email.timestamp}</div>
        `;

        // Change background color if the email is read
        email_div.style.backgroundColor = email.read ? '#f0f0f0' : '#ffffff';

        // Add event listener to open email when clicked
        email_div.addEventListener('click', () => open_email(email.id));

        // Style for better display
        email_div.style.borderBottom = '1px solid #ddd';
        email_div.style.padding = '10px';
        email_div.style.cursor = 'pointer';
        
        // Add this email's div to the emails view
        document.querySelector('#emails-view').append(email_div);
      });
    })
    .catch(error => console.log("Error al cargar correos:", error));
}

// Function to open and display the content of a single email
function open_email(email_id) {

  // Fetch the email details
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {

      // Clear out the emails view and show email content
      document.querySelector('#emails-view').innerHTML = `
        <div><strong>De:</strong> ${email.sender}</div>
        <div><strong>Para:</strong> ${email.recipients}</div>
        <div><strong>Asunto:</strong> ${email.subject}</div>
        <div><strong>Fecha:</strong> ${email.timestamp}</div>
        <hr>
        <div>${email.body}</div>
      `;

      // Mark email as read if it's not already
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({ read: true })
        });
      }
    })
    .catch(error => console.log("Error al abrir el correo:", error));
}
