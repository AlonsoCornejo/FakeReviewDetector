from webapp.mixins import CRUDMixin
from flask_login import UserMixin

from webapp import db

import random

'''
    Much of this code is used to create python objects for SQLAlchemy and then easily input or read data from the DB.
    We need these classes only for SQLAlchemy, but we should not be using them to add/drop tables, or edit their
    structure since we have moved to a persistent mySQL DB on Xie's server. All add/drop/edit should be happening in 
    the mySQL terminal ideally.
'''

ROLE_USER = 0
ROLE_ADMIN = 1


# defines user logic for db, needs to be optimized
class User(UserMixin, CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(512))
    role = db.Column(db.SmallInteger, default=random.randint(2, 3))
    s1 = db.Column(db.Boolean)
    s1_background = db.Column(db.Boolean)
    s2 = db.Column(db.Boolean)
    s3 = db.Column(db.Boolean)
    s4 = db.Column(db.Boolean)
    lastSeen = db.Column(db.String(255))

    def __init__(
            self,
            email=None,
            password=None,
            s1=False,
            s1_background=False,
            s2=False,
            s3=False,
            s4=False,
            role=None):
        self.email = email
        self.password = password
        self.s1 = s1
        self.s1_background = s1_background
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.role = role

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    # determine which model to display
    def is_clearModel(self):
        if self.role == 2:
            return True
        elif self.role == 3:
            return False

    def is_active(self):
        return True

    def get_id(self):
        # return unicode(self.id)
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.email)


# main survey before entering site
class Survey1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_used = db.Column(db.String(255))  # (1) multiple choice

    # familarity = db.Column(db.Float) # (2) range slider

    used_radio = db.Column(db.String(255))  # Multiple Choice
    tech_radio = db.Column(db.String(255))  # Multiple Choice
    agree_radio = db.Column(db.String(255))  # Multiple Choice
    agree_radio2 = db.Column(db.String(255))  # Multiple Choice
    likely_radio = db.Column(db.String(255))  # Multiple Choice
    often_radio = db.Column(db.String(255))  # Multiple Choice
    often_radio2 = db.Column(db.String(255))  # Multiple Choice
    confident_radio = db.Column(db.String(255))  # Multiple Choice
    confident_radio2 = db.Column(db.String(255))  # Multiple Choice

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey1')

    def __init__(
            self,
            ai_used=None,
            used_radio=None,
            tech_radio=None,
            agree_radio=None,
            agree_radio2=None,
            likely_radio=None,
            often_radio=None,
            often_radio2=None,
            confident_radio=None,
            confident_radio2=None):
        self.ai_used = ai_used
        self.used_radio = used_radio
        self.tech_radio = tech_radio
        self.agree_radio = agree_radio
        self.agree_radio2 = agree_radio2
        self.likely_radio = likely_radio
        self.often_radio = often_radio
        self.often_radio2 = often_radio2
        self.confident_radio = confident_radio
        self.confident_radio2 = confident_radio2

    def get_id(self):
        return self.id


class Background(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    confident = db.Column(db.String(255))  # Multiple Choice

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='background')

    def __init__(
            self,
            confident=None):
        self.confident = confident

    def get_id(self):
        return self.id

#need to link this to mySQL instead of sqlite
class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    confident = db.Column(db.String(255))  # Multiple Choice

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='training')

    def __init__(
            self,
            confident=None):
        self.confident = confident

    def get_id(self):
        return self.id

#need to link this to mySQL instead of sqlite
class Testing(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    opinion = db.Column(db.String(255))  # Multiple Choice
    confident = db.Column(db.Float)  # Range Slider
    prediction = db.Column(db.String(255))  # Multiple Choice

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='testing')

    def __init__(
            self,
            opinion=None,
            confident=None,
            prediction=None):
        self.opinion = opinion
        self.confident = confident
        self.prediction = prediction

    def get_id(self):
        return self.id

#class ForgotPassword(db.Model):

#class TestingResult():

# class for the feedback form
class Feedback(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # foreign key from user table
    user = db.relationship('User', uselist=False, backref='feedback')
    stars = db.Column(db.Integer, primary_key=True)  # star rating from the form
    openFeedback = db.Column(db.String(191), primary_key=True)  # feedback field from the form

    def __init__(
            self,
            id=None,
            stars=None,
            openFeedback=None):
        self.id = id
        self.stars = stars
        self.openFeedback = openFeedback

    def get_id(self):
        return self.id

    def get_stars(self):
        return self.stars

    def get_feedback(self):
        return self.openFeedback
