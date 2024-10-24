---

# 🎨 Image Forgery Detection Using ORB and SSIM 🖼️

Welcome to the **Image Forgery Detection** project! This application allows users to compare two images and detect whether they have been tampered with or forged using powerful algorithms such as **ORB (Oriented FAST and Rotated BRIEF)** for feature matching and **SSIM (Structural Similarity Index Measure)** for similarity comparison.

![](https://github.com/user-attachments/assets/b5c2d2bb-1573-40af-b62a-c66edce9e0da)
![](https://github.com/user-attachments/assets/8ae52715-fcf5-42e3-be63-f6306840e14c)
![](https://github.com/user-attachments/assets/fd1c9af9-8098-4065-a2e0-5618749c57e9)

---

## 🚀 Features

- **Drag-and-drop interface** to upload images 🎯
- Detect image tampering with **ORB feature matching** 🔍
- Compare image similarity using **SSIM** algorithm 📊
- Real-time comparison with **MD5 hash verification** 🔑
- Auto-deletion of uploaded files to keep your environment clean 🧹
- A simple, user-friendly **web interface** built with **Flask** 🌐

---

## 🏗️ Tech Stack

This project is built using the following technologies:

- **Flask**: A lightweight WSGI web application framework for Python
- **Flask-CORS**: To enable Cross-Origin Resource Sharing (CORS) in the Flask app
- **OpenCV (cv2)**: For image processing and ORB feature extraction
- **Pillow (PIL)**: To work with images, including resizing and format conversion
- **NumPy**: For matrix and array manipulation, used alongside OpenCV and SSIM
- **scikit-image (SSIM)**: For computing the structural similarity between images

---

## 🎯 How It Works

The system uses two powerful algorithms to detect image forgery:

### 🔍 ORB (Oriented FAST and Rotated BRIEF)
ORB is a fast, keypoint-based algorithm that detects features in images and matches them across different images. If an image has been altered or forged, the number of matched keypoints will differ significantly.

### 📊 SSIM (Structural Similarity Index Measure)
SSIM is a perceptual metric that quantifies image quality degradation by comparing two images and detecting differences in structure, luminance, and contrast. SSIM values range from `0 to 1`, where `1` indicates identical images and `0` indicates no similarity.

### 🔑 MD5 Hashing
The MD5 algorithm is used to generate a unique fingerprint (hash) for each image. If two images have the same hash, they are identical. This provides a quick way to check for identical images without doing pixel-by-pixel comparisons.

---

## 🖥️ How to Use

1. **Clone the Repository** 📦:

    ```bash
    git clone https://github.com/yourusername/image-forgery-detection.git
    cd image-forgery-detection
    ```

2. **Install the Dependencies** 🛠️:

    Use the provided `requirements.txt` file or manually install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, install the packages manually:

    ```bash
    pip install Flask flask-cors opencv-python numpy scikit-image Pillow werkzeug
    ```

3. **Run the Application** 🎮:

    Start the Flask development server:

    ```bash
    python app.py
    ```

    The app will be running on `http://127.0.0.1:5000`. Open it in your web browser and start detecting forgeries!

4. **Upload Images** 🖼️:

    - Click on the "Choose File" button to upload two images.
    - Alternatively, you can **drag and drop** images into the boxes provided.

5. **Compare Images** 🔍:

    - After uploading, click on the **Compare Images** button.
    - The application will compute the similarity using **SSIM**, check for keypoint matches using **ORB**, and verify the **MD5 hashes** of the images.

6. **View Results** 📝:

    - The app will display the results on the same page, including:
      - Whether the images are identical or forged.
      - The **MD5 hash** of each image.
      - The **SSIM index**.
      - The number of **ORB keypoint matches**.

---

## 💡 Code Structure

Here’s a breakdown of the most important files and what they do:

```bash
image-forgery-detection/
├── app.py                  # The main Flask app and backend logic
├── static/
│   ├── css/
│   │   └── styles.css       # Custom CSS for styling the frontend
│   ├── js/
│   │   └── script.js        # JavaScript for frontend interactivity (image preview, form submission)
│   ├── images/              # Placeholder and icon images
├── templates/
│   ├── index.html           # Main frontend page for uploading and comparing images
│   ├── about.html           # About page with developer information
└── uploads/                 # Temporary folder to hold uploaded images
```

### app.py 📜

- **Flask Setup**: Initializes the Flask app, routes, and file-handling configuration.
- **Image Comparison**:
  - **SSIM**: Used to compare the structure of the two images.
  - **ORB**: Used to match keypoints between the two images.
- **File Management**:
  - Uploaded files are stored temporarily in the `uploads/` folder.
  - Files are deleted immediately after the comparison process to avoid clutter.
  
---

## 🛠️ Customization

Feel free to customize the app to suit your needs. Some ideas for further improvements include:

- **Add more forgery detection algorithms**: You could integrate other methods such as Error Level Analysis (ELA) for more precise forgery detection.
- **Improved UI/UX**: The interface can be further enhanced with more animations or using a frontend framework like React.
- **Deploying the App**: You can deploy the app to a platform like **Heroku** or **AWS EC2** for public use.

---

## 📜 API Documentation

### POST `/compare`

This route compares two uploaded images for forgery detection. The API accepts two image files and returns the comparison results.

#### Request

- Method: **POST**
- Content-Type: **multipart/form-data**
- Form Data:
  - `image1`: The first image to compare.
  - `image2`: The second image to compare.

#### Response

- Status: **200 OK**
- JSON Structure:

    ```json
    {
      "hash1": "md5-hash-of-image-1",
      "hash2": "md5-hash-of-image-2",
      "ssim_index": 0.99,
      "orb_matches": 100,
      "result": "Images are identical."
    }
    ```

---

## 🤖 About Us

Meet the developers behind this project:

### Developer 1: Siddhanth Oleti 🧑‍💻
- **B.Tech Information Technology** @ Manipal Institute of Technology
- ![LinkedIn](./static/images/linkedin-icon.png) [LinkedIn](https://linkedin.com)
- ![GitHub](./static/images/github-icon.png) [GitHub](https://github.com)

### Developer 2: Shivaram Kumar J 🧑‍💻
- **B.Tech Information Technology**
- ![LinkedIn](./static/images/linkedin-icon.png) [LinkedIn](https://linkedin.com)
- ![GitHub](./static/images/github-icon.png) [GitHub](https://github.com)

*Hobbyist developers with a passion for building cool stuff! 😎✨*

---

## 🤝 Contributions

Feel free to contribute to the project by:

- **Opening issues** for any bugs or suggestions.
- **Submitting pull requests** for improvements and new features.

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 🎉 Thank You

Thank you for using the Image Forgery Detection app! We hope this helps you in identifying image tampering and forgeries. If you have any feedback or feature requests, feel free to open an issue or reach out to us.

---
