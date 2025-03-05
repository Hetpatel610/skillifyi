const navToggle = document.getElementById("nav-toggle");
const navLinks = document.getElementById("nav-links");

navToggle.addEventListener("click", () => {
  navLinks.classList.toggle("active");
});

function searchFunction() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let boxes = document.getElementsByClassName("box");

  for (let box of boxes) {
    let title = box.getElementsByTagName("h2")[0].textContent.toLowerCase();
    box.style.display = title.includes(input) ? "" : "none";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  fetchResources();
});

function fetchResources() {
  fetch("/users/api/events/")
      .then(response => response.json())
      .then(data => {
          const container = document.getElementById("resource-container");
          container.innerHTML = ""; // Clear existing content

          data.resources.forEach(event => {
              let box = document.createElement("div");
              box.classList.add("resource-box"); // Proper class for styling

              let title = document.createElement("h3");
              title.textContent = event.title;
              box.appendChild(title);

              let description = document.createElement("p");
              description.textContent = event.description;
              box.appendChild(description);

              if (resource.file) {
                  let link = document.createElement("a");
                  link.href = event.file;
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
