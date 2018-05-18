from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import Topic, Post

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

@app.route("/topics")
def topics():
    return render_template('topics.html', topics=Topic.query.all(), title='Topics')

@app.route("/topic/<topic_name>")
def topic(topic_name):
    topic = Topic.query.filter_by(topicname=topic_name).first()
    return render_template('topic.html', topic=topic)

# @app.route("/post")



# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html', title='404'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html', title='500'), 500
