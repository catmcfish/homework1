// Function to update the display of navbar links based on window width
function updateNavbarLinks() {
    // If the window width is less than 650 pixels
    if (window.innerWidth < 650) {
        // Get all anchor elements within the navbar
        let links = document.getElementsByClassName("navbar a");
        // Loop through each link and hide it
        for (let i = 0; i < links.length; i++) {
            links[i].style.display = "none";
        }
        // Display the menu image
        document.getElementById("menuImg").style.display = "block";
    } else {
        // Get all anchor elements within the navbar
        let links = document.getElementsByClassName("navbar a");
        // Loop through each link and display it
        for (let i = 0; i < links.length; i++) {
            links[i].style.display = "flex";
        }
        // Hide the menu image
        document.getElementById("menuImg").style.display = "none";
    }
}

// Add event listener to update navbar links when the DOM content is loaded
document.addEventListener('DOMContentLoaded', updateNavbarLinks);

// Add event listener to update navbar links when the window is resized
window.addEventListener('resize', updateNavbarLinks);

// Add event listener to toggle the vertical navbar when the menu image is clicked
document.getElementById("menuImg").addEventListener('click', function() {
    // Check if the clicked element is the menu image
    if(event.target.id == "menuImg") {
        // Toggle the display of the vertical navbar
        if (document.getElementById("verticalNavbar").style.display == "flex") {
            document.getElementById("verticalNavbar").style.display = "none";
        }
        else {
            document.getElementById("verticalNavbar").style.display = "flex";
        }
    }
});