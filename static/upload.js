document.getElementById('upload-button').addEventListener('click', function() {
    console.log('Button clicked');
    var fileInput = document.getElementById('file-input');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('image', file);

    // Send the form data to the server using AJAX or fetch API
    // Example using fetch API:
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        console.log(data);
    })
    .catch(error => {
        // Handle any errors that occur during the request
        console.error(error);
    });
});