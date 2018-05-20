from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import Topic, Post


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



# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html', title='404'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html', title='500'), 500
