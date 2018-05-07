from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
# from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f"User('{self.topicname}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



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

# Debug
if __name__ == '__main__':
    app.run(debug=True)
