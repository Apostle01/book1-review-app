
https://git.heroku.com/padomabook-review-app.git
https://apostle01.github.io/book1-review-app/
# [book1-review-app Screenshot of the website.](/docs/am-i-responsive.png)

book1-review-app is a simple web application for managing reviews. Users can view, add, and edit book reviews, but only administrators can delete them.



## Features

-User registration and login
-Add new book reviews
-Edit existing book reviews
-Delete book reviews (Adminiatrator only)
-Custom 404 error page

## Installaation

1. Clone the repository

'''sh
git clone https://github.com/your-username/book1-review-app.git
cd book1-review-app

2. Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate # on windows use 'venv\Scripts\activate'

3. Install the dependencies
    pip install -r requirements.txt

4. Set up the database:
    flask db upgrade

5. Run the application:
    python app.py

Deployment on Heroku

1. Install thee Heroku CLI if you haven't already
    curl https://cli-assets.heroku.com/install.sh | sh

2. Log in to your Heroku account:
    heroku login

3. Create a new Heroku application
    heroku create your-app-name

4. Add a PostgresSQL database to your Heroku app:
    heroku addons:create heroku-postgresql:hobby-dev

5. Set the 'Flask-App' and 'Flask_ENV' configuration variables on Heroku:
    heroku config:set Flask_App=app.py
    heroku config:set Flask_ENV=production

6. Initialize the database on Heroku:
    heroku run flask db upgrade

7. Deploy the application to Heroku:
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main

Usage

Open your web browser and navigate to 'https://your-app-name.herokuapp.com' to access the application

Routes
. `/register`:Register a new user
. `/login`:Login for existing users
. `/logout`:Logout the current user
. `/`:View all book reviews and add new ones (if logged in)
. `/edit/<int:id>`:Edit a book review (admin only)
. `/delete/<int:id>`:Delete a book review (admin only)

Administrator Privilages

To give a user administrator privilages,  you need to manually update the database. You can do this by running a Python shell within your Flask app context on Heroku:
    heroku run flask shell

Then execute the following commands:
    from models import User
    User = User.query.filter_by(username='your_admin_username').first()
    user.is_admin = True
    db.session.commit()

Replace your_admin_username with the username of the user you want to promote to administrator.

Error Handling

A custom 404 page is provided for handling non-existent routes. You can customize this page by editing the '404.html' file in thee template directoru.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contributing

If you have any questions or suggestions, feel free to contact the project maintainer at nanaafianyameke2@gmail.com.

This 'README.md' provides comprehesive instructions for local setup and Heroku deployment,
making it easy for others to understand and deploy your app. Adjust the placeeholder values accordingly.
