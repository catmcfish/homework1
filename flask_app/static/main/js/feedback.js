document.addEventListener('DOMContentLoaded', function() {
    const feedbackBtn = document.getElementById('feedbackBtn');
    const feedbackForm = document.getElementById('feedbackForm');
    const closeBtn = document.getElementById('closeFeedback');
    const feedbackFormElement = feedbackForm.querySelector('form');

    // Show feedback form when button is clicked
    feedbackBtn.addEventListener('click', function() {
        feedbackForm.style.display = 'block';
    });

    // Hide feedback form when close button is clicked
    closeBtn.addEventListener('click', function() {
        feedbackForm.style.display = 'none';
    });

    // Hide feedback form when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === feedbackForm) {
            feedbackForm.style.display = 'none';
        }
    });

    // Handle form submission - let the browser handle the form submission naturally
    // This allows the server-side redirect to work properly
    feedbackFormElement.addEventListener('submit', function(event) {
        // Don't prevent default - let the form submit normally
        // The server will handle the redirect to the feedback page
        
        // Close the feedback form modal
        feedbackForm.style.display = 'none';
    });
});
