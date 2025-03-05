const navToggle = document.getElementById("nav-toggle");
const navLinks = document.getElementById("nav-links");

navToggle.addEventListener("click", () => {
  navLinks.classList.toggle("active");
});

function searchTitles() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let resourceBoxes = document.querySelectorAll(".resource-box");

  resourceBoxes.forEach(box => {
      let title = box.querySelector(".title").innerText.toLowerCase();
      if (title.includes(input)) {
          box.style.display = "block";
      } else {
          box.style.display = "none";
      }
  });
}


document.addEventListener("DOMContentLoaded", function () {
  fetchResources();
});

function fetchResources() {
  fetch("/users/api/resources/")
      .then(response => response.json())
      .then(data => {
          const container = document.getElementById("resource-container");
          container.innerHTML = ""; // Clear existing content

          data.resources.forEach(resource => {
              let box = document.createElement("div");
              box.classList.add("resource-box"); // Proper class for styling

              let title = document.createElement("h3");
              title.textContent = resource.title;
              box.appendChild(title);

              let description = document.createElement("p");
              description.textContent = resource.description;
              box.appendChild(description);

              if (resource.file) {
                  let link = document.createElement("a");
                  link.href = resource.file;
                  link.textContent = "Download";
                  link.classList.add("details-btn"); // Corrected class name
                  link.setAttribute("download", "");
                  box.appendChild(link);
              }

              // ✅ Directly Append to Container (No extra div)
              container.appendChild(box);
          });
      })
      .catch(error => console.error("Error fetching resources:", error));
}
