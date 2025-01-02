from app import create_app
from flask import Flask, jsonify, request, render_template
import pandas as pd

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
