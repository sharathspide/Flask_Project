document.addEventListener('DOMContentLoaded', function() {
    //text transform get user input
    const submitButton = document.getElementById('submit-button');
    const userInputField = document.getElementById('user-input');
    const responseParagraph = document.getElementById('response');
    //youtube link get user input
    const linkSubmitButton = document.getElementById('sbt_button');
    const linkInput = document.getElementById('link');
    const filenameInput = document.getElementById('filename');
    const youtubeResponse = document.getElementById('youTube_response');

    submitButton.addEventListener('click', function() {
        const userInput = userInputField.value;

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            responseParagraph.textContent = 'Processed Data: ' + data.processed_data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    linkSubmitButton.addEventListener('click', function() {
        const userLinkInput = linkInput.value;
        const userFilenameInput = filenameInput.value;

        fetch('/download',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: [JSON.stringify({ link: userLinkInput}), JSON.stringify({filename: userFilenameInput })]
        })
        .then(response => response.json())
        .then(data => {
            youtubeResponse.textContent = data.processed_data;
        }).catch(error => {
            console.error('Error:', error);
        });
    });   
});
