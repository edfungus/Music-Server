from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir
from queue import Queue

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

queue = Queue()

from app import views, models
