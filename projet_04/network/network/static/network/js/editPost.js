document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".edit-btn").forEach(button => {
      button.onclick = () => {
          const postId = button.dataset.postId;
          const postContent = document.querySelector(`.post-content[data-post-id='${postId}']`);
          
          // Reemplazar contenido con un área de texto
          const textarea = document.createElement("textarea");
          textarea.className = "form-control";
          textarea.value = postContent.innerHTML.trim();
          postContent.replaceWith(textarea);

          // Cambiar el botón a "Guardar"
          button.innerText = "Save";
          button.onclick = () => {
              fetch(`/edit_post/${postId}`, {
                  method: "PUT",
                  headers: {
                      "Content-Type": "application/json",
                      "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                  },
                  body: JSON.stringify({ content: textarea.value })
              })
              .then(response => response.json())
              .then(data => {
                  if (data.error) {
                      alert(data.error);
                  } else {
                      const newContent = document.createElement("p");
                      newContent.className = "card-text post-content";
                      newContent.dataset.postId = postId;
                      newContent.innerHTML = textarea.value;
                      textarea.replaceWith(newContent);
                      button.innerText = "Edit";
                      button.onclick = button.originalOnClick;
                  }
              });
          };
      };
  });
});
