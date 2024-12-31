from flask import request, jsonify, Blueprint, render_template, current_app
import os
from model.preprocess import get_books
from flask import render_template, Blueprint

# Create a Blueprint
routes = Blueprint("routes", __name__)

# Route to serve the frontend
@routes.route('/')
def home():
    return render_template('index.html')


# Route to get books from an image
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

'''
@routes.route('/get_books', methods=['POST'])
def get_books_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded image
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
    print(f"Resolved file path: {image_path}")
    image.save(image_path)
    print("File saved successfully.")

    output_folder = os.path.join('SPECTaiCLE', 'runs', 'detect', 'predict', 'crops', 'Book')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        predicted_books = get_books(image_file_paths=image_path)
        return jsonify({'predicted_books': predicted_books})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''   


@routes.route('/get_books', methods=['POST'])
def get_books_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400
    
    
    # Save the uploaded image
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    image_path = os.path.join(upload_folder, image.filename)
    print(f"Saving file to: {image_path}")

    image.save(image_path)
    print("File saved successfully.")

    try:
        predicted_books = get_books(image_path)
        return jsonify({'predicted_books': predicted_books})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
