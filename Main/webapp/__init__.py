import os
import sqlite3
import mysql.connector

from flask import Flask, render_template, request, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize and configure flask app
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from webapp import views
from webapp import models
from webapp.models import User
# db.drop_all()
# db.create_all()
db.session.commit()
# Main method for webapp deploy
if __name__ == '__main__':
    db.create_all()

    db.session.commit()
    users = User.query.all()
    db.session.commit()
    app.run(debug=True)
