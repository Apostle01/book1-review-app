from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    books = db.relationship('Book', backref='owner', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_link = db.Column(db.String(300), nullable=False)
    amazon_link = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    book = db.relationship('Book', backref=db.backref('comments', lazy=True))
