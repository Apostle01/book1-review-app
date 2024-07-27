from flask import render_template, url_for, flash, redirect
from app import app, db
from app.forms import RegistrationForm, LoginForm, BookForm
from app.models import User, Book

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

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    if form.validate_on_submit():
        # Update user account
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    return render_template('account.html', form=form)
