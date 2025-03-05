const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');

navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active'); // Toggle the 'active' class to show/hide the menu
});
document.getElementById('menu-icon').addEventListener('click', function() {
  document.getElementById('nav-links').classList.toggle('active');
});

document.addEventListener('DOMContentLoaded', function () {
    const profileList = document.getElementById('profile-list');

    const fetchProfiles = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/profiles/', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),  // assuming token-based auth
                    'Content-Type': 'application/json',
                },
            });
            const profiles = await response.json();
            
            profiles.forEach(profile => {
                const li = document.createElement('li');
                li.textContent = `${profile.first_name} ${profile.last_name}`;
                profileList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching profiles:', error);
        }
    };

    fetchProfiles();
});
