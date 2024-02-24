$(document).ready(function() {
    $('#submit').click(function() {

        // Get the input value
        const coursesInput = $('#courses');
        const courses = coursesInput.val();

        // Make an AJAX request to the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/schedule',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ courses }),      // key is courses
            success: function(response) {
                console.log('Backend response:', response.result);
                $("#result").html("Result: " + response.result);
    
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });
});
