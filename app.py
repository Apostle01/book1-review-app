import os
from flask import Flask, app, render_template, url_for, flash, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, BookForm, CommentForm
from app import db, Users, Book, Comment
from app.routes import app_bp # type: ignore
from config import Config
import logging

def create_app():
    app = Flask(__name__)

# Use environment variables for configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your_secret_key")

# Select the database based on development status
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri or "postgresql://postgres:Admin@localhost/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(app_bp)

    return app

# with app.app_context():
#     db.create_all()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    messages = ["Welcome to the Book Review App!", "Enjoy your stay!"]
    return render_template('home.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8
        )
        new_user = Users(
            username=form.username.data, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        amazon_link = (
            f"https://www.amazon.com/s?tag=faketag&k="
            f"{form.name.data.replace(' ', '+')}"
        )
        new_book = Book(
            name=form.name.data,
            author=form.author.data,
            details=form.details.data,
            price=form.price.data,
            image_link=form.image_link.data,
            amazon_link=amazon_link
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully', 'success')
        return redirect(url_for('search'))
    return render_template('add_book.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()
    return render_template(
        'search.html', books=books, search_query=search_query
    )

@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()

    return render_template(
        'delete_book.html', books=books, search_query=search_query
    )

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        try:
            # Delete associated comments
            Comment.query.filter_by(book_id=book.id).delete()
            db.session.delete(book)
            db.session.commit()
            flash(f'Book "{book.name}" deleted successfully', 'success')
            return redirect(url_for('delete_book'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error deleting book: {e}')
            flash(
                f'An error occurred while trying to delete the book: {str(e)}',
                'danger'
            )

    return render_template('confirm_delete.html', book=book)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, book_id=book.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
    return render_template('book_details.html', book=book, form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
