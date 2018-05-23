from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import Topic, Post
from flaskblog.forms import RegistrationForm, LoginForm


# Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/topics")
def topics():
    return render_template('topics.html', topics=Topic.query.all(), title='Topics')

@app.route("/topic/<topic_name>")
def topic(topic_name):
    topic = Topic.query.filter_by(topicname=topic_name).first()
    return render_template('topic.html', topic=topic)

@app.route("/post/<post_title>")
def post(post_title):
    post = Post.query.filter_by(title=post_title).first()
    topic = Topic.query.filter_by(id=post.topic_id).first()
    return render_template('post.html', topic=topic, post=post)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Log In', form=form)
