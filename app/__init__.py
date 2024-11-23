from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import app_bp  # Import the app_bp Blueprint

# Initialize the database globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration for the app
    app.config['SECRET_KEY'] = 'f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60'  # Replace with your secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost/books'  # Replace with your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the db with the app
    db.init_app(app)

    # Register the Blueprint
    app.register_blueprint(app_bp)

    return app
