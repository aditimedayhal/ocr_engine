from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ocr_engine import process_pdf, extract_text_from_image

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for React frontend)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file is allowed (PDF or image)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        if filename.lower().endswith('.pdf'):
            # Process PDF and convert to images
            image_paths = process_pdf(filename)
            texts = []
            for image_path in image_paths:
                text = extract_text_from_image(image_path)
                texts.append(text)
            return jsonify({'texts': texts})
        else:
            # Extract text from image
            text = extract_text_from_image(filename)
            return jsonify({'text': text})

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
