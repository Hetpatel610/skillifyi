document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();  // Prevent default form submission

    const formData = new FormData(this);
    const actionUrl = this.getAttribute('action');  // Form's action URL

    fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;  // Redirect on successful login
        } else {
            alert(data.error_message);  // Show error message
        }
    })
    .catch(error => console.error('Error:', error));
});
