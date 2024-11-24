import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the database globally
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuration for the app
    app.config['SECRET_KEY'] = 'f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60'  # Replace with your secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost/books'  # Replace with your database URI
    app.config['AMAZON_BASE_URL'] = os.environ.get('AMAZON_BASE_URL', 'https://www.amazon.com/s?tag=faketag&k=')

    # Initialize the db with the app
    db.init_app(app)
    # login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Specify login route for @login_required

    # Register the Blueprint
    from app.routes import app_bp  # Ensure app.routes defines `app_bp`
    app.register_blueprint(app_bp)

    return app
