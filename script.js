document.getElementById('uploadButton').addEventListener('click', async function () {
    const textInput = document.getElementById('textInput').value;
    const fileInput = document.getElementById('fileUpload').files[0];
    const outputText = document.getElementById('outputText');

    if (!fileInput && !textInput) {
        alert("Please provide either text or a file to extract text.");
        return;
    }

    const formData = new FormData();
    if (fileInput) formData.append('file', fileInput);
    if (textInput) formData.append('text', textInput);

    // Show a temporary loading message
    outputText.value = "Extracting text... Please wait.";

    try {
        const response = await fetch('http://localhost:8000/ocr', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to extract text');
        }

        const data = await response.json();
        outputText.value = data.text;  // Display extracted text

    } catch (error) {
        console.error('Error:', error);
        outputText.value = 'An error occurred while processing the file.';
    }
});