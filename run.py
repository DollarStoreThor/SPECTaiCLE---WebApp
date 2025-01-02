from app import create_app
from flask import Flask, jsonify, request, render_template
import pandas as pd

app = create_app()

@app.route('/')
def index():
    # Read CSV file
    df = pd.read_csv(r"C:\Users\arado\Desktop\SPECTaiCLE\model\recommendation_csv_files\b.csv")
    
    # Extract unique values for dropdown
    dropdown_options = df['AuthorTitleString'].unique().tolist()
    
    # Sort options alphabetically (optional)
    dropdown_options.sort()
    
    return render_template('index.html', dropdown_options=dropdown_options)

if __name__ == "__main__":
    app.run(debug=True)
