from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.forms import RegistrationForm, LoginForm, BookForm
from app.models import User, Book
from flask_migrate import Migrate
from flask_login import LoginManager


@app.route('/')
@app.route('/home')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        # Authentication logic
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

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

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    if form.validate_on_submit():
        # Update user account
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    return render_template('account.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
return render_template('404.html'), 404  # type: ignore

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, Debug=True)

