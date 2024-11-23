from flask import Flask
from app.routes import app_bp  # Import the app_bp Blueprint

def create_app():
    app = Flask(__name__)

    # Add secret key for session management (use an environment variable for production)
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key in production

    # Register the Blueprint
    app.register_blueprint(app_bp)

    return app

# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost/postgres'
# app.config['SECRET_KEY'] = 'your_secret_key_here'

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# login_manager = LoginManager(app)

# from app import routes, models
# app.register_blueprint(routes.bp)
# from app import routes, models
# app.register_blueprint(routes.bp)


# from app import routes, models
