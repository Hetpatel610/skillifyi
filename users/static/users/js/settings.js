// Function to update profile details (name, bio, profile picture)
function updateProfile() {
  const formData = new FormData(document.getElementById("updateProfileForm"));
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/users/update-profile/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Profile updated successfully!");
      } else {
        alert("Error: " + JSON.stringify(data.errors));
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Function to change the password
function changePassword() {
  const formData = new FormData(document.getElementById("changePasswordForm"));
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/users/change-password/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => response.json())  // Expecting a JSON response
    .then((data) => {
      if (data.success) {
        alert("Password changed successfully!");
      } else {
        // Display validation errors from the backend (if any)
        if (data.errors) {
          const errors = data.errors;
          // Handle errors (e.g., display errors on the form)
          if (errors.old_password) {
            document.getElementById('oldPasswordError').textContent = errors.old_password;
          }
          if (errors.new_password) {
            document.getElementById('newPasswordError').textContent = errors.new_password;
          }
          if (errors.confirm_password) {
            document.getElementById('confirmPasswordError').textContent = errors.confirm_password;
          }
        } else {
          alert("An unknown error occurred.");
        }
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An unexpected error occurred. Please try again.");
    });
}

function getCSRFToken() {
  let csrfToken = null;
  const cookies = document.cookie.split("; ");
  for (let cookie of cookies) {
      if (cookie.startsWith("csrftoken=")) {
          csrfToken = cookie.split("=")[1];
      }
  }
  return csrfToken;
}

// ✅ Logout Function
function logoutUser() {
  fetch("/users/api/logout/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken()  // 🔥 CSRF Token Add Karo
      },
      credentials: "include"
  })
  .then(response => response.json())
  .then(data => {
      console.log("Logout Response:", data);
      alert(data.message);
      window.location.href = "/users/login/"; // Redirect to home
  })
  .catch(error => console.error("Logout error:", error));
}



// ✅ Delete Account Function
function deleteAccount() {
  if (!confirm("Are you sure you want to delete your account?")) return;

  fetch("/users/api/delete-account/", {
      method: "DELETE",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken()  // 🔥 CSRF Token Add Karo
      },
      credentials: "include"
  })
  .then(response => response.json())
  .then(data => {
      console.log("Delete Account Response:", data);
      alert(data.message);
      window.location.href = "/users/signup"; // Redirect after delete
  })
  .catch(error => console.error("Delete Account error:", error));
}


