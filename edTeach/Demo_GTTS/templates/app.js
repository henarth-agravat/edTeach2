function transcribeVideo() {
    var fileInput = document.getElementById('videoInput');
    var file = fileInput.files[0];

    if (!file) {
        alert('Please select a video file.');
        return;
    }

    var formData = new FormData();
    formData.append('file', file);

    $.ajax({
        type: 'POST',
        url: '/transcribe',
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
            $('#transcriptionResult').text(data);
        },
        error: function(xhr, status, error) {
            alert('An error occurred while transcribing the video.');
            console.error(error);
        }
    });
}