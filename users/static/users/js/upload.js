function showFields() {
  const type = document.getElementById("upload-type").value;
  const dynamicFields = document.getElementById("dynamic-fields");
  const dateField = document.getElementById("date-field");

  if (type) {
    dynamicFields.style.display = "block";
  } else {
    dynamicFields.style.display = "none";
  }

  if (type === "event") {
    dateField.style.display = "block";
  } else {
    dateField.style.display = "none";
  }
}

// Handle Form Submission with JavaScript
document.getElementById("uploadForm").addEventListener("submit", function (event) {
  event.preventDefault();

  let formData = new FormData(this);
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  // 🔥 Debug: Check if URL is null
  const formActionUrl = this.getAttribute("data-action-url");
  if (!formActionUrl) {
      alert("Error: Form action URL is missing!");
      return;
  }

  fetch(formActionUrl, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },
  })
  .then((response) => response.json())
  .then((data) => {
      console.log("Response:", data);
      if (data.status === "success") {
          alert("Upload successful!");
      } else {
          alert("Error: " + JSON.stringify(data.errors));
      }
  })
  .catch((error) => {
      console.error("Error:", error);
      alert("An unexpected error occurred.\n" + error.message);
  });
});
