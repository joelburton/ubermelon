import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# The Flask application
app = Flask(__name__)
app.config.from_object('config')

# Database Connection
db = SQLAlchemy(app)
