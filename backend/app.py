import os
import hashlib
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder and allowed extensions
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@app.route('/compare', methods=['POST'])
def compare_images():
    logger.info('Received a request to compare images.')
    if 'image1' not in request.files or 'image2' not in request.files:
        logger.error('Two images were not uploaded.')
        return jsonify({'error': 'Please upload two images.'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        logger.error('One or both images have no filename.')
        return jsonify({'error': 'No selected file(s).'}), 400

    if image1 and allowed_file(image1.filename) and image2 and allowed_file(image2.filename):
        # Generate unique filenames to prevent collisions
        unique_filename1 = f"{uuid.uuid4()}_{secure_filename(image1.filename)}"
        unique_filename2 = f"{uuid.uuid4()}_{secure_filename(image2.filename)}"
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename2)
        
        try:
            # Save the uploaded images
            image1.save(filepath1)
            image2.save(filepath2)
            logger.info(f"Saved image1 as {filepath1}")
            logger.info(f"Saved image2 as {filepath2}")
        except Exception as e:
            logger.error(f"Error saving images: {e}")
            return jsonify({'error': 'Failed to save uploaded images.'}), 500

        # Check if files exist before hashing
        if not os.path.exists(filepath1):
            logger.error(f"File {filepath1} does not exist after saving.")
            return jsonify({'error': f'Failed to save {image1.filename}'}), 500
        if not os.path.exists(filepath2):
            logger.error(f"File {filepath2} does not exist after saving.")
            return jsonify({'error': f'Failed to save {image2.filename}'}), 500

        # Compute MD5 hashes
        hash1 = compute_md5(filepath1)
        hash2 = compute_md5(filepath2)
        logger.info(f"Computed MD5 for image1: {hash1}")
        logger.info(f"Computed MD5 for image2: {hash2}")

        # Attempt to delete the files
        for filepath in [filepath1, filepath2]:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    logger.info(f"Deleted {filepath}")
                except Exception as e:
                    logger.error(f"Error deleting {filepath}: {e}")
            else:
                logger.warning(f"File {filepath} does not exist and cannot be deleted.")

        # Compare hashes
        if hash1 == hash2:
            result = 'Images are identical.'
        else:
            result = 'Images are different or forged.'

        logger.info(f"Comparison result: {result}")

        return jsonify({
            'hash1': hash1,
            'hash2': hash2,
            'result': result
        }), 200
    else:
        logger.error('Invalid file type uploaded.')
        return jsonify({'error': 'Invalid file type. Allowed types are png, jpg, jpeg, gif.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
