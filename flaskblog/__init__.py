from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
admin = Admin(app)



from flaskblog import routes
from flaskblog.models import Topic, Post

admin.add_view(ModelView(Topic, db.session))
admin.add_view(ModelView(Post, db.session))
