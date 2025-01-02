from flask import request, jsonify, Blueprint, render_template, current_app
import os
from model.preprocess import get_books
from model.recommendations import get_recommendations #need to create this python script
from flask import render_template, Blueprint
import pandas as pd

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
        predicted_books = get_books(correctImages=True, cullNullTextImages=False, image_file_paths=[image_path])
        return jsonify({'predicted_books': predicted_books})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@routes.route('/get_dropdown_data', methods=['GET'])
def get_dropdown_data():
    try:
        # Load your CSV file
        file_path = r"C:\Users\arado\Desktop\SPECTaiCLE\model\recommendation_csv_files\b.csv"  # Replace with your actual CSV file path
        df = pd.read_csv(file_path)

        # Extract unique elements from the specific column
        unique_elements = df['AuthorTitleString'].dropna().unique()  # Replace 'ColumnName' with your column name

        # Convert to a list and return as JSON
        return jsonify({'unique_elements': unique_elements.tolist()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@routes.route('/get_recommendations', methods=['POST'])
def get_recommendations_route():
    try:
        # Parse the JSON payload
        data = request.get_json()
        if not data or "book_name" not in data:
            return jsonify({"error": "No book name provided"}), 400

        book_name = data["book_name"].strip()
        if not book_name:
            return jsonify({"error": "Book name cannot be empty"}), 400

        # Call your function to generate recommendations
        recommended_books = get_recommendations()

        # Return the recommendations
        return jsonify({"recommended_books": recommended_books}), 200
    except Exception as e:
        # Log the error for debugging
        print(f"Error in /get_recommendations: {e}")
        return jsonify({"error": str(e)}), 500