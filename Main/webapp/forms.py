# all the forms and surveys used
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, RadioField, DecimalField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Email, Regexp, Length, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import IntegerRangeField, DecimalRangeField
from wtforms import Form
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from webapp.models import User
import hashlib
from . import db


# ensures login so data can be stored with username
def validate_login(form, field):
    # Get user info from the form on screen
    user = form.get_user()
    # Check that there was a user inputted
    if user is None:
        raise ValidationError('User not found.')
    # Hash the inputted password from the form and compare it to the hash saved in the DB as a hex string
    hashed_form_pass = hashlib.sha512(form.password.data.encode()).hexdigest()
    if user.password != hashed_form_pass:
        raise ValidationError('Invalid login')


# Logic to log in an existing user
class LoginForm(FlaskForm):
    # check email and password, ensuring there is an input to the field
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), validate_login])

    # method to get the first user from the DB by a query on the email input into the form
    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()


# may be redundant with added page in views
class ForgotPasswordForm(FlaskForm):
    email = StringField("Input your email",validators=[InputRequired(), Email()])

### what else could go here? do I query here?
    def get_Password(self):
        return "this is a test password"

    def get_Email(self):
        #return email
        return "chrismunoz1019@gmail.com"

    # Check the DB for any duplicate users and throw an error if yes.
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=self.email.data).count() <= 0:
            raise ValidationError('Unknown Email')



# signing up
class RegistrationForm(FlaskForm):
    # check that all the required fields are set properly
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    consent = BooleanField(validators=[InputRequired()])
    password = PasswordField('New Password', [InputRequired(),
                                              Length(min=6, max=20),
                                              EqualTo('confirm', message='Password Required')])
    confirm = PasswordField(validators=[InputRequired()])

    # Check the DB for any duplicate users and throw an error if yes.
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=self.email.data).count() > 0:
            raise ValidationError('Duplicate email')


# Logic to set a new password
class NewPass(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), Length(min=8, max=20),
                                              EqualTo('confirm', message='Password Required')])
    confirm = PasswordField(validators=[InputRequired()])


# questions for main survey
class Survey1Form(FlaskForm):
    ai_used = RadioField('',
                         choices=[('Y', 'Yes'), ('N', 'No')],
                         validators=[InputRequired()], default=None)
    used_radio = RadioField('',
                            choices=[('A', 'I am unfamiliar with its capabilities'),
                                     ('B', 'I am mostly unfamiliar with its capabilities'),
                                     ('C', 'I am somewhat familiar with its capabilities'),
                                     ('D', 'I am mostly familiar with its capabilities')])
    tech_radio = RadioField('',
                            choices=[('A', 'I use technology in my daily life (ex: computer, phone, etc.)'),
                                     ('B', 'I have more than 5 years of experience using technology.'),
                                     ('C', 'I wish to learn more about AI technology.'),
                                     ('D', 'I do not use technology.')])
    agree_radio = RadioField('',
                             choices=[('A', 'Completely Agree'),
                                      ('B', 'Agree'),
                                      ('C', 'Disagree'),
                                      ('D', 'Completely Disagree')])
    agree_radio2 = RadioField('',
                              choices=[('A', 'Completely Agree'),
                                       ('B', 'Agree'),
                                       ('C', 'Disagree'),
                                       ('D', 'Completely Disagree')])
    likely_radio = RadioField('',
                              choices=[('A', 'Very Likely'),
                                       ('B', 'Likely'),
                                       ('C', 'Unlikely'),
                                       ('D', 'Very Unlikely')])
    often_radio = RadioField('',
                             choices=[('A', 'Very Often'),
                                      ('B', 'Often'),
                                      ('C', 'Not Often'),
                                      ('D', 'Very rarely')])
    often_radio2 = RadioField('',
                              choices=[('A', 'Very Often'),
                                       ('B', 'Often'),
                                       ('C', 'Not Often'),
                                       ('D', 'Very rarely')])
    confident_radio = RadioField('',
                                 choices=[('A', 'Very Confident'),
                                          ('B', 'Confident'),
                                          ('C', 'Unconfident'),
                                          ('D', 'Very Unconfident')])
    confident_radio2 = RadioField('',
                                  choices=[('A', 'Very Confident'),
                                           ('B', 'Confident'),
                                           ('C', 'Unconfident'),
                                           ('D', 'Very Unconfident')])


class BackgroundForm(FlaskForm):
    confident = RadioField('Are you ready to see some reviews and learn more about spam spotting?',
                           choices=[('Y', 'Yes! Move on to the next step!'),
                                    ('N', 'No not yet, I think I\'ll check out the research more first')],
                           validators=[InputRequired()], default=None)


class FeedbackForm(FlaskForm):
    stars = RadioField('How many stars would you give the website from 1-5?',
                       choices=[('1', '1 Star'),
                                ('2', '2 Stars'),
                                ('3', '3 Stars'),
                                ('4', '4 Stars'),
                                ('5', '5 Stars')],
                       validators=[InputRequired()], default=None)
    openFeedback = StringField('Please use this space to leave any comments or suggestions on the site.')


class TrainingForm(FlaskForm):
    confident = RadioField(
        'Are you confident to move on to the next step of testing out spams based on the above explanation?',
        choices=[('Y', 'Yes! Move on to the next step!'), ('N', 'No not yet, I think I\'ll check out the research more first')],
        validators=[InputRequired()], default=None)


class TestingForm(FlaskForm):
    opinion = RadioField('What\'s your opinion?', choices=[('G', 'Genuine'), ('F', 'Fake')],
                         validators=[InputRequired()], default=None)
    confident = DecimalRangeField('0 - 10', [InputRequired(), NumberRange(min=0, max=10)])
    prediction = RadioField('Reveal SpEagle Prediction', choices=[('G', 'Genuine'), ('F', 'Fake')], default='G')

class SpEagleForm(FlaskForm):
  	pid = h5fields.IntegerField('Please input a product ID', widget=h5widgets.NumberInput(min=0, max=200), validators=[InputRequired()])
   # uid = IntegerField('Please select a user ID', validators=[InputRequired(), NumberRange(min=0,max=200)])
    #loop = True
    #while(loop):
     #   if(uid. > 200):
      #      uid = IntegerField('Please select a user ID', validators=[InputRequired(), NumberRange(min=0,max=200)])
       # elif(uid._value < 0):
        #    uid = IntegerField('Please select a user ID', validators=[InputRequired(), NumberRange(min=0,max=200)])
        #else:
         #   loop = False

class PBeliefForm(FlaskForm):
  	#notrsure
		"test"
	