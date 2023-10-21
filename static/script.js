document.addEventListener('DOMContentLoaded', function() {


    // swap button colours in interest.html

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

    if (checkboxes) {
        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                var labelId = 'label-' + this.id;
                var label = document.getElementById(labelId);
                console.log('Checkbox changed:', this.value);

                if (this.checked) {
                    label.classList.remove('btn-outline-dark');
                    label.classList.add('btn-outline-light');
                } else {
                    label.classList.remove('btn-outline-light');
                    label.classList.add('btn-outline-dark');
                }
            });
        });
    }




    // or scroll if arrow is clicked
    var arrow = document.getElementById('arrow'); // Find the arrow icon by its class
    if (arrow) {
        arrow.addEventListener('click', function() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        });
    }

    // Auto scroll after 7 seconds
    if (arrow) {
        setTimeout(function() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }, 6000);
    }


    // Change heart icon when selected/deselected and send an AJAX request
    // Select all elements with class 'fa-heart'
    var hearts = document.querySelectorAll('.fa-heart');

    // Loop through each heart element
    if (hearts) {
        hearts.forEach(function(heart) {
            heart.addEventListener('click', function() {
                // Get the course ID from the 'data-course-id' attribute
                var courseId = this.getAttribute('data-course-id');

                // Check if the heart has the 'fa' class (indicating it's liked)
                var isLiked = this.classList.contains('fa');

                // Make an AJAX request to update the liked status in the database
                fetch('/like_course', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            courseId: courseId,
                            isLiked: !isLiked // Invert the liked status (like/unlike)
                        })
                    })
                    .then(response => response.json()) // Parse the response as JSON
                    .then(data => {
                        // If the server successfully updated the liked status
                        if (data.status === 'success') {
                            // Change the heart icon class based on the liked status
                            if (!isLiked) {
                                this.classList.remove('fa-regular'); // Remove outline heart
                                this.classList.add('fa'); // Add solid heart
                            } else {
                                this.classList.remove('fa'); // Remove solid heart
                                this.classList.add('fa-regular'); // Add outline heart
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            });
        });
    }


     // Automatically submit drop-down select menu when an option is clicked in the recommendation page
     document.querySelector('select').addEventListener('change', function() {
        document.querySelector('form').submit();
    });



});