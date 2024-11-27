document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn").forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
            fetch(`/toggle_like/${postId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    button.innerText = data.liked ? "Unlike" : "Like";
                    const likeCount = document.querySelector(`.like-count[data-post-id='${postId}']`);
                    if (likeCount) {
                        likeCount.innerText = data.like_count;
                    }
                }
            })
            .catch(error => console.error("Error:", error));
        };
    });
});


// Helper function to get CSRF token
function getCSRFToken() {
    const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]') || 
                         document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.content || tokenElement.value : null;
}
