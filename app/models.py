from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    image_link = db.Column(db.String(300), nullable=True)
    amazon_link = db.Column(db.String(300))
    comments = db.relationship('Comment', backref='book', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    book = db.relationship('Book', backref=db.backref('comments', lazy=True))
