// Custom JavaScript for the Student Enrollment System

// Add active class to current navigation item
document.addEventListener("DOMContentLoaded", function () {
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll(".navbar .nav-link");

    navLinks.forEach((link) => {
        const linkPath = link.getAttribute("href");
        if (
            currentLocation === linkPath ||
            (linkPath !== "/" && currentLocation.startsWith(linkPath))
        ) {
            link.classList.add("active");
        }
    });

    // Initialize date picker fields if needed
    const dateFields = document.querySelectorAll('input[type="date"]');
    if (dateFields.length > 0) {
        console.log("Date fields initialized");
    }

    // Add form validation if needed
    const forms = document.querySelectorAll(".needs-validation");
    if (forms.length > 0) {
        Array.from(forms).forEach((form) => {
            form.addEventListener(
                "submit",
                function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add("was-validated");
                },
                false
            );
        });
    }
});

// Function to confirm delete actions
function confirmDelete(event, message) {
    if (!confirm(message || "Are you sure you want to delete this item?")) {
        event.preventDefault();
        return false;
    }
    return true;
}
