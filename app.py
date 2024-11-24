import os
import logging
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from dotenv import load_dotenv
from app.forms import RegistrationForm, LoginForm, BookForm, UpdateAccountForm
from app.models import User, Book, Comment
from app import create_app

# Load environment variables
load_dotenv()

# Initialize the app
app = create_app()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
@app.route('/home')
def home():
    """Homepage with paginated book listings."""
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=10)
    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """View details of a specific book."""
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    """Add a new book."""
    form = BookForm()
    if form.validate_on_submit():
        amazon_link = f"{app.config['AMAZON_BASE_URL']}{form.name.data.replace(' ', '+')}"
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
        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for books."""
    search_query = request.form.get('search', '')
    books = Book.query.filter(Book.name.contains(search_query)).all() if search_query else []
    return render_template('search.html', books=books, search_query=search_query)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    """Delete a specific book."""
    book = Book.query.get_or_404(book_id)
    try:
        Comment.query.filter_by(book_id=book.id).delete()
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting book ID {book.id}: {str(e)}', exc_info=True)
        flash('An error occurred while deleting the book.', 'danger')
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """Manage user account."""
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
    return render_template('account.html', title='Account', form=form)


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
