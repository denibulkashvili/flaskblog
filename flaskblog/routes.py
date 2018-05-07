from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import Topic, Post
# from forms import RegistrationForm, LoginForm


posts = [
    {
        'author': 'Denis',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'May 5th, 2018'
    },
    {
        'author': 'User',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 5th, 2018'
    }
]

# Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash('Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)

# @app.route("/login")
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Login', form=form)
