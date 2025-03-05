document.getElementById("npiForm").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission

  // Collect form data
  let formData = new FormData(this);

  const formActionUrl = this.getAttribute("data-action-url"); // Correct reference to form
  fetch(formActionUrl, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        alert("Name and Profile Image saved successfully!");
      } else {
        alert("Failed: " + JSON.stringify(data.errors));
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An unexpected error occurred. Please try again.");
    });
});

// Show file name when an image is selected
document.getElementById("profileImage").addEventListener("change", function () {
  const fileName = this.files[0].name;
  document.getElementById("fileName").textContent = fileName;
});
