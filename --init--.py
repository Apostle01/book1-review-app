from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/alive_tank_path_776536')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    with app.app_context():
        from app import routes, models
        db.create_all()

    return app

