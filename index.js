/**
 * Open a dialog to select an image from the device
 * @param {boolean} openCamera True, if the capture tag should be added to the input field to open the camera 
 */
function selectImage(openCamera) {
    const input = document.getElementById("image-input");
    if (openCamera) {
        input.setAttribute("capture", "camera");
    }
    else {
        input.removeAttribute("cature");
    }

    // trigger the click event of the input to select a Image
    input.click();
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
    const submitButton = document.getElementById("submit-btn");
    submitButton.innerHTML = "Wird hochgeladen..."
    submitButton.disabled = true;
    // image to submit
    const input = document.getElementById("image-input");
    const image = input.files[0];

    // API URL
    const url = "http://" + window.location.hostname + ":8000";

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
            alert(data);
        }
    })
    .catch((error) => {
        alert(error);
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
    submitButton.innerHTML = "Hochladen";
    submitButton.disabled = false;
}