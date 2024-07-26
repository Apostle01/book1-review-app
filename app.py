from flask import Flask, render_template, url_for, flash, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, BookForm, CommentForm
from models import db, Users, Book, Comment
from config import Config
import logging
import os

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Use environment variables for configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or 'a_default_fallback_secret_key'

# Select the database based on development status
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

db.init_app(app)

with app.app_context():
    db.create_all()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            return redirect(url_for('home'))  # type: ignore
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)  # type: ignore

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
        return redirect(url_for('login'))  # type: ignore
    return render_template('register.html', form=form)  # type: ignore

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))  # type: ignore

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
        return redirect(url_for('search'))  # type: ignore
    return render_template('add_book.html', form=form)  # type: ignore

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()
    return render_template(  # type: ignore
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

    return render_template(  # type: ignore
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
            return redirect(url_for('delete_book'))  # type: ignore
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error deleting book: {e}')
            flash(
                f'An error occurred while trying to delete the book: {str(e)}',
                'danger'
            )

    return render_template('confirm_delete.html', book=book)  # type: ignore

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, book_id=book.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
    return render_template('book_details.html', book=book, form=form)  # type: ignore

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # type: ignore

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,)
