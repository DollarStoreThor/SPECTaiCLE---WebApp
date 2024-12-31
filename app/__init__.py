from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow cross-origin requests

    # Import and register the Blueprint
    from .routes import routes
    app.register_blueprint(routes)

    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")

    return app
