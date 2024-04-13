/**
 * Open a dialog to select an image from the device
 */
function selectImage() {
    // trigger the click event of the input to select a Image
    document.getElementById("image-input").click();
}

/**
 * Take a Image by the camera
 */
function takeImage() {
    var constraints = { video: true };

    navigator.mediaDevices.getUserMedia(constraints)
        .then(function(mediaStream) {
            var video = document.createElement('video');
            video.srcObject = mediaStream;
            video.onloadedmetadata = function(e) {
                video.play();
                var canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                var context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                var image = canvas.toDataURL('image/jpeg');
                showPreview(image);
                mediaStream.getTracks().forEach(track => track.stop());
            };
        })
        .catch(function(err) {
            console.error('Error accessing camera:', err);
        });
}

/**
 * Show a preview of the image
 */
function showPreview() {
    // get the input element and select the first image
    const input = document.getElementById("image-input");
    const image = input.files[0];
    // get the preview image and set the src attribute
    const imgTag = document.getElementById("preview");
    imgTag.src = URL.createObjectURL(image);
    // show submit button
    const submitButton = document.getElementById("submit-btn");
    submitButton.style.visibility = "visible";
}

/**
 * Submit image to API
 */
function submit() {
    // image to submit
    const input = document.getElementById("image-input");
    const image = input.files[0];

    // API URL
    const url = "http://localhost:8000";

    // create FormData and add image
    const formData = new FormData();
    formData.append("image", image);

    // send POST-Request
    fetch(url, {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.msg === "Success"){
            // show message box with success text
            const msgBox = document.getElementById("msg-box");
            msgBox.style.visibility = "visible";
            // disable pointer events
            const container = document.getElementById("container");
            container.style.pointerEvents = "none";
        }
        else {
            console.log('Response:  ', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Close the message box displaying feedback from the API
 */
function closeMessageBox() {
    // hide message box with success text
    const msgBox = document.getElementById("msg-box");
    msgBox.style.visibility = "hidden";
    // enable pointer events
    const container = document.getElementById("container");
    container.style.pointerEvents = "all";
    // reset preview
    const imgTag = document.getElementById("preview");
    imgTag.src = "UploadIcon.png";
    // reset input to prevent storing hundreds of images
    const imgInput = document.getElementById("image-input");
    imgInput.value = "";
    // hide submit button
    const submitButton = document.getElementById("submit-btn");
    submitButton.style.visibility = "hidden";
}