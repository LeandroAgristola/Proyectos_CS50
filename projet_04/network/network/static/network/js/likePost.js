document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn").forEach(button => {
        button.addEventListener("click", () => {
            const postId = button.dataset.postId;
            const liked = button.dataset.liked === "true";

            fetch(`/toggle_like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }

                // Update the like count
                const likeCount = document.querySelector(`.like-count[data-post-id="${postId}"]`);
                likeCount.textContent = data.like_count;

                // Update button text and state
                button.dataset.liked = data.liked;
                button.textContent = data.liked ? "Unlike" : "Like";
            })
            .catch(error => console.error("Error:", error));
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    const cookies = document.cookie.split(";").map(cookie => cookie.trim());
    for (let cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}
