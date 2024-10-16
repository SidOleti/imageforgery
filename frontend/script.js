document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            console.log('Submit event triggered.');
            e.preventDefault(); // Prevent the default form submission
            console.log('Default form submission prevented.');
    
            const image1 = document.getElementById('image1').files[0];
            const image2 = document.getElementById('image2').files[0];
    
            if (!image1 || !image2) {
                displayResult('Please select both images.', 'error');
                return;
            }
    
            const formData = new FormData();
            formData.append('image1', image1);
            formData.append('image2', image2);
    
            try {
                console.log('Sending POST request to backend...');
                const response = await fetch('http://localhost:5000/compare', {
                    method: 'POST',
                    body: formData
                });
    
                if (!response.ok) {
                    // If the response is not a 2xx status, throw an error
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Unknown server error');
                }
    
                const data = await response.json();
                console.log('Received response from backend:', data);
    
                if (data.error) {
                    displayResult(data.error, 'error');
                } else {
                    displayResult(data.result, data.result === 'Images are identical.' ? 'success' : 'error');
                }
            } catch (error) {
                console.error('Error during fetch:', error);
                displayResult(error.message || 'An error occurred while processing.', 'error');
            }
            console.log('End of submit event handler.');
        });
    } else {
        console.error("Form with ID 'upload-form' not found.");
    }
});

function displayResult(message, type) {
    const resultDiv = document.getElementById('result');
    if (resultDiv) {
        resultDiv.textContent = message;
        resultDiv.className = type;
        // Log the display result for debugging
        console.log(`Displaying result: ${message} of type: ${type}`);
    } else {
        console.error("Result div with ID 'result' not found.");
    }
}
