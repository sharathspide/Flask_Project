document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submit-button');
    const userInputField = document.getElementById('user-input');
    const responseParagraph = document.getElementById('response');

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
});
