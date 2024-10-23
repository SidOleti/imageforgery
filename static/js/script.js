document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');
    const metricsDiv = document.getElementById('metrics');
    const submitButton = document.getElementById('submit-button');

    // Bind file input change event to previewImage function
    const imageInput1 = document.getElementById('image1');
    const imageInput2 = document.getElementById('image2');
    
    // Attach event listeners for file input changes
    imageInput1.addEventListener('change', function(event) {
        previewImage(event, 'drop-area1', 'plus-icon1', 'text1', 'preview1');
    });
    imageInput2.addEventListener('change', function(event) {
        previewImage(event, 'drop-area2', 'plus-icon2', 'text2', 'preview2');
    });

    // Handle form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const image1 = document.getElementById('image1').files[0];
            const image2 = document.getElementById('image2').files[0];

            // Check if both images are selected
            if (!image1 || !image2) {
                displayResult('Please select both images.', 'error');
                return;
            }

            // Prepare form data
            const formData = new FormData();
            formData.append('image1', image1);
            formData.append('image2', image2);

            // Show loading state
            displayResult('Comparing images...', 'loading');
            submitButton.disabled = true;

            try {
                // Send POST request to backend
                const response = await fetch('/compare', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Unknown server error');
                }

                // Process the response
                const data = await response.json();
                displayResult(data.result, data.result === 'Images are identical.' ? 'success' : 'error');
                displayMetrics(data);

            } catch (error) {
                displayResult(error.message, 'error');
            } finally {
                submitButton.disabled = false;
            }
        });
    }

    // Preview image function
    function previewImage(event, dropAreaId, plusIconId, textId, previewId) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            // When the file is loaded, preview it
            reader.onload = function(e) {
                console.log('Image loaded successfully:', e.target.result);  // Debugging

                const plusIcon = document.getElementById(plusIconId);
                const text = document.getElementById(textId);
                const preview = document.getElementById(previewId);

                // Hide the placeholder text and icon
                plusIcon.style.display = 'none';
                text.style.display = 'none';

                // Show the image preview
                preview.src = e.target.result;  // Set the src to the file's base64 data
                preview.style.display = 'block';  // Ensure the image is visible

                console.log('Preview image updated.');  // Debugging
            };

            reader.readAsDataURL(file);  // Read the image as data URL
        } else {
            console.error('No file selected!');  // Debugging
        }
    }

    // Display result message
    function displayResult(message, type) {
        resultDiv.textContent = message;
        resultDiv.className = `message ${type}`;
    }

    // Display additional metrics
    function displayMetrics(data) {
        metricsDiv.innerHTML = `
            <p><strong>MD5 Hash 1:</strong> ${data.hash1}</p>
            <p><strong>MD5 Hash 2:</strong> ${data.hash2}</p>
            <p><strong>SSIM Index:</strong> ${data.ssim_index || 'N/A'}</p>
            <p><strong>ORB Matches:</strong> ${data.orb_matches || 'N/A'}</p>  <!-- Show ORB Matches -->
        `;
    }
    
});
