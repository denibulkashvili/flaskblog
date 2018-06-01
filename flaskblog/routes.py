import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.models import Topic, Post, User
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required


# Routes
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/topics")
def topics():
    topics = Topic.query.all()
    return render_template('topics.html', topics=topics, title='Topics')

@app.route("/topic/<topic_name>")
def topic(topic_name):
    topic = Topic.query.filter_by(topicname=topic_name).first()
    return render_template('topic.html', topic=topic)


@app.route("/post/<post_title>")
def post(post_title):
    post = Post.query.filter_by(title=post_title).first()
    topic = Topic.query.filter_by(id=post.topic_id).first()
    return render_template('post.html', title=post.title, topic=topic, post=post)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new post"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user,
                    topic_id=form.topic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                            form=form, legend='New Post')

@app.route("/post/<post_title>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_title):
    """Update posts"""
    post = Post.query.filter_by(title=post_title).first()
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_title=post.title))
    # populate title and content with existin data in post
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content


    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post')

@app.route("/post/<post_title>/delete", methods=['POST'])
@login_required
def delete_post(post_title):
    """Delete posts"""
    post = Post.query.filter_by(title=post_title).first()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    """Save user uploaded pictures to file system"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext  # picture filename
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    # resize image with pillow
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title="Account",
                            image_file=image_file, form=form)
