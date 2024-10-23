import os
import hashlib
import uuid
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image
from logging import Logger as logger

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def orb_feature_matching(image_path1, image_path2):
    # Load images in grayscale
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        logger.error("One of the images could not be loaded.")
        return 0, "N/A"

    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=500)

    # Detect keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Check if descriptors were found
    if des1 is None or des2 is None:
        logger.error("No descriptors found in one or both images.")
        return 0, "N/A"

    # Use BFMatcher to match descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    if not matches:
        logger.error("No matches found between the images.")
        return 0, "N/A"

    # Sort matches by distance (lower distance is better)
    matches = sorted(matches, key=lambda x: x.distance)
    logger.info(f"Keypoints in image 1: {len(kp1) if kp1 else 0}, Keypoints in image 2: {len(kp2) if kp2 else 0}")

    logger.info(f"ORB matches found: {len(matches)}")
    return len(matches), matches  # Return the number of matches



def compute_ssim(image_path1, image_path2):
    # Open images using PIL and convert to grayscale
    image1 = Image.open(image_path1).convert('L')
    image2 = Image.open(image_path2).convert('L')
    
    # Resize images to the same size
    image1 = image1.resize((min(image1.size[0], image2.size[0]), min(image1.size[1], image2.size[1])))
    image2 = image2.resize((image1.size[0], image1.size[1]))  # Ensure both are the same size
    
    # Convert back to numpy arrays for SSIM calculation
    image1 = np.array(image1)
    image2 = np.array(image2)
    
    # Compute SSIM between the two images
    ssim_index, _ = ssim(image1, image2, full=True)
    return ssim_index


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_images():
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Please upload two images.'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1 and allowed_file(image1.filename) and image2 and allowed_file(image2.filename):
        unique_filename1 = f"{uuid.uuid4()}_{secure_filename(image1.filename)}"
        unique_filename2 = f"{uuid.uuid4()}_{secure_filename(image2.filename)}"
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename2)

        image1.save(filepath1)
        image2.save(filepath2)

        ssim_index = compute_ssim(filepath1, filepath2)
        hash1 = compute_md5(filepath1)
        hash2 = compute_md5(filepath2)

        result = 'Images are identical.' if hash1 == hash2 else 'Images are different or forged.'
        
        os.remove(filepath1)
        os.remove(filepath2)

        return jsonify({
            'hash1': hash1,
            'hash2': hash2,
            'ssim_index': ssim_index,
            'result': result
        }), 200
    else:
        return jsonify({'error': 'Invalid file type.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
