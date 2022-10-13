# handles most of the sits routing
import hashlib
import smtplib,ssl
import uuid
import json
import os.path
from datetime import date, datetime
from email.message import EmailMessage

from flask import render_template, flash, redirect, session
from flask import url_for, g, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_paginate import Pagination, get_page_args
from flask_sqlalchemy import get_debug_queries

from webapp import app, db, lm
from .config import DATABASE_QUERY_TIMEOUT
from .forms import LoginForm, RegistrationForm, Survey1Form, BackgroundForm, TrainingForm, TestingForm, FeedbackForm, ForgotPasswordForm, SpEagleForm, PBeliefForm
from .models import User, Survey1, Background, Training, Testing, Feedback
import json


from email.mime.multipart import MIMEMultipart
from time import sleep

from . import scrapping

from pydoc import describe
from flask import Flask, redirect, url_for, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.utils import redirect

@app.route('/')
@app.route('/index')  # home page routing
def index():
    user = g.user
    return render_template("index.html", title="Home", user=user)


# Display registration page on GET to /register. Also allow POSTing to this route on submit form
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Pull up the registration form from forms.py
    form = RegistrationForm(request.form)
    # On success (i.e. no errors) input the fresh username, password, and newly generated UID to the DB
    if form.validate_on_submit():
        # create user object from models.py with the given parameters from the form.
        user = User(email=form.email.data, password=hashlib.sha512(form.password.data.encode()).hexdigest())
        # Add and commit the new user object to the DB with SQLAlchemy.
        db.session.add(user)
        db.session.commit()
        # Log in the new user using the Flask login library
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title="Create Account", form=form)


@app.route('/forgotPasswordSend/', methods=['GET', 'POST'])
def forgotPasswordSend():
     # Get the template for the page from forms.py
    form = ForgotPasswordForm(request.form)
   
    forgottenPass = form.get_Password()
    sendToemail = form.get_Email() #get this from form, then check password in db
    print(sendToemail)
    msg = EmailMessage()
    message = """

    Hello, you requested your forgotten password from our site. Please let us know if this was not you.\n\


       Password: """ + forgottenPass 
     
    msg.set_content(message)
   
    gmail_user = 'spamspotting@gmail.com'
    gmail_password = 'spamspotter123'
    sent_from = gmail_user
    to = [sendToemail]

    msg['From'] = gmail_user
    msg['To'] = sendToemail
    msg['Subject'] = 'Spam Spotting Password Recovery'
   
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print ('Email sent!')
    return render_template('/interfaces/ForgotPassword.html', title="Forgot Password", form=form)

# Display forgot password page and send an email on request. Can GET the page, and POST on submit form.
@app.route('/forgotPassword/', methods=['GET', 'POST'])
def forgotPassword():

    form = ForgotPasswordForm(request.form)
    return render_template('/interfaces/ForgotPassword.html', title="Forgot Password", form=form)


@app.route('/termsAndConditions/', methods=['GET', 'POST'])
def termsAndConditions():
    form=BackgroundForm(request.form)
    return render_template('interfaces/TermsAndConditions.html', title="Terms And Conditions",form=form)
    #return redirect(url_for('termsAndConditions'))
    #nothing
    
# Display the login page, and again allow GET to page and POST on submit form.
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Get the login template from forms.py
    form = LoginForm(request.form)
    # Ensure the user info on the login form is correct
    if form.validate_on_submit():
        # If so, log in said user using Flask
        user = form.get_user()  # login routing and functionality
        login_user(user)
        # TODO: Why is this if block here? What does it do.
        if current_user.is_admin():
            return redirect(url_for('index'))
        else:
            return redirect(url_for("index"))
    return render_template('login.html', title="Login", form=form)


@app.route('/survey_1/', methods=['GET', 'POST'])
@login_required
def survey_1():
    g.user = current_user
    if g.user.s1_background is False:
        form = Survey1Form(request.form)

        if form.validate_on_submit():
            survey = Survey1()
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)

            g.user.s1_background = True
            g.user.s1 = True
            g.user.lastSeen = date.today()
            db.session.commit()
            return redirect(url_for('background'))

        return render_template('interfaces/Survey1.html', title='Survey', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/background/', methods=['GET', 'POST'])
def background():
    #g.user = current_user
    form = BackgroundForm(request.form)
    if form.confident.data == 'Y':  # fixes issue of going to paginate on yes or no
        return redirect(url_for('paginate'))
    elif form.confident.data == 'N':
        return redirect(url_for('research'))  # send to reserach if not ready for reviews

    return render_template('interfaces/Background.html', title='Background', form=form)


@app.route('/sandbox/', methods=['GET', 'POST'])
def sandbox():
                form = SpEagleForm(request.form)
                # if request.form.get("sort"):
                #       pID = form.pid.data
                #       return  redirect(url_for('run_speagle', pData=pID))
                if request.method == 'POST':
                        if request.form['submit_button'] == 'Run SpEagle':
                                        if form.validate_on_submit():
                                                my_path = os.path.abspath(os.path.dirname(__file__))
                                                file_path = os.path.join(my_path, "../AI/data/yelp_features.json")
                                                userdata = open(file_path)
                                                jdata = json.load(userdata)
                                                userdata.close()
                                                pID = form.pid.data
                                                value = jdata[str(pID)]['prod']
                                                value['userid'] = pID
                                                value['MNR'] = round(float(value['MNR']),3)
                                                value['PR'] = round(float(value['PR']),3)
                                                value['NR'] = round(float(value['NR']),3)
                                                value['avgRD'] = round(float(value['avgRD']),3)
                                                value['ERD'] = round(float(value['ERD']),3)
                                                value['ETG'] = round(float(value['ETG']),3)
                                                return render_template('interfaces/Sandbox.html', userinfo=value, form=form)
                        elif request.form['submit_button'] == 'View All Reviews':
                                        if form.validate_on_submit():
                                                pID = form.pid.data
                                                return  redirect(url_for('run_speagle', pData=pID))
                        else:
                                        pass # unknown
                elif request.method == 'GET':
                        return render_template('interfaces/Sandbox.html', form=form)
                
@app.route('/run_speagle/<pData>', methods=['GET', 'POST'])
def run_speagle(pData):
                output = ""
                my_path = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(my_path, "../AI/data/yelp_data.json")
                file_name = open(file_path)
                data = json.load(file_name)
                file_name.close()
                product = data[pData]
                count = 0
                sorted_values = sorted(product.values()) # Sort the values
                sorted_dict = {}
                keys = list(product.keys())
                for i in sorted_values:
                        for k in product.keys():
                                        if product[k] == i and k not in sorted_dict:
                                                        sorted_dict[k] = i
                                                        break
                
                for uID in sorted_dict:
                        count = count + 1
                        pr = (count / len(sorted_dict)) * 100
                        product[uID] = pr
                        #output += "USER ID: " + uID + " - PRECENTILE RANK: " +  str(product.get(uID)) + "\n"

                for uID in product:
                        output += "USER ID: " + uID + " - PERCENTILE RANK: " + "%.4f" % product.get(uID) + "\n"

                output = output.split('\n')
                output.pop()
                return render_template('interfaces/PBeliefValues.html', processed_text=output, keys=keys, pData=pData)

@app.route('/run_speagle_high/<pData>', methods=['GET', 'POST'])
def run_speagle_high(pData):
                output = ""
                my_path = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(my_path, "../AI/data/yelp_data.json")
                file_name = open(file_path)
                data = json.load(file_name)
                file_name.close()
                product = data[pData]
                count = 0
                sorted_values = sorted(product.values()) # Sort the values
                sorted_dict = {}
                for i in sorted_values:
                                for k in product.keys():
                                                if product[k] == i and k not in sorted_dict:
                                                                sorted_dict[k] = product[k]
                                                                break

                keys = list(sorted_dict.keys()) 
                keys = keys[::-1]                       
                for uID in sorted_dict:
                        count = count + 1
                        pr = (count / len(sorted_dict)) * 100
                        product[uID] = pr

                for uID in reversed(sorted_dict):
                        output += "USER ID: " + uID + " - PERCENTILE RANK: " + "%.2f" % product.get(uID) + "\n" 
        
                output = output.split('\n')
                output.pop()
                return render_template('interfaces/PBeliefValues.html', processed_text=output,  keys=keys, pData=pData) 

@app.route('/run_speagle_low/<pData>', methods=['GET', 'POST'])
def run_speagle_low(pData):
                output = ""
                my_path = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(my_path, "../AI/data/yelp_data.json")
                file_name = open(file_path)
                data = json.load(file_name)
                file_name.close()
                product = data[pData]
                count = 0
                sorted_values = sorted(product.values()) # Sort the values
                sorted_dict = {}
                keys = list(product.keys())
                for i in sorted_values:
                                for k in product.keys():
                                                if product[k] == i and k not in sorted_dict:
                                                                sorted_dict[k] = product[k]
                                                                break

                keys = list(sorted_dict.keys())         
                for uID in sorted_dict:
                        count = count + 1
                        pr = (count / len(sorted_dict)) * 100
                        product[uID] = pr

                for uID in sorted_dict:
                        output += "USER ID: " + uID + " - PERCENTILE RANK: " + "%.2f" % product.get(uID) + "\n" 
        
                output = output.split('\n')
                output.pop()
                return render_template('interfaces/PBeliefValues.html', processed_text=output, keys=keys, pData=pData)          

@app.route('/dive_in/<pData>/<uData>', methods=['GET', 'POST'])
def dive_in(pData, uData):
                output = ""
                my_path = os.path.abspath(os.path.dirname(__file__))
                file_path = os.path.join(my_path, "../AI/data/yelp_features.json")
                file_name = open(file_path)
                data = json.load(file_name)
                file_name.close()
                product = data[pData]
                userReview = product[uData]

                value = {}
                userReview['userid'] = uData
                userReview['RD'] = round(float(userReview['RD']), 5)
                # value['EXT'] =  userReview['EXT']
                # value['DEV'] = userReview['DEV']
                # value['ETF'] = userReview['ETF']
                # value['ISR'] = userReview['ISR']
                
                output = output.split('\n')
                return render_template('interfaces/DiveIn.html', userinfo=userReview)


# @app.route('/newpage/', methods=['GET', 'POST'])
# def newpage():
#     my_path = os.path.abspath(os.path.dirname(__file__))
#     file_path = os.path.join(my_path, "static\yelp_features.json")
#     userdata = open(file_path)
#     jdata = json.load(userdata)
#     userdata.close()
#     if request.method == 'GET':
#         return render_template('interfaces/newpage.html', title='newpage')
#     if request.method == 'POST':
#         userid = request.form['userid']
#         value = jdata[str(userid)]['prod']
#         value['userid'] = userid
#         value['MNR'] = round(float(value['MNR']),3)
#         value['PR'] = round(float(value['PR']),3)
#         value['NR'] = round(float(value['NR']),3)
#         value['avgRD'] = round(float(value['avgRD']),3)
#         value['ERD'] = round(float(value['ERD']),3)
#         value['ETG'] = round(float(value['ETG']),3)
#         return render_template('interfaces/newpage.html', title='newpage', userinfo=value)


@app.route('/research/', methods=['GET', 'POST'])  # routing logic, page needs content
def research():
    g.user = current_user
    #if g.user.s1_background is not False:
    form = BackgroundForm(request.form)

    if form.validate_on_submit():
        survey = Background()
        form.populate_obj(survey)
        #survey.user = g.user
        db.session.add(survey)

        #g.user.s1 = True
        #g.user.lastSeen = date.today()
        db.session.commit()
        # logout_user()
        # return redirect(url_for('logouthtml'))
        return redirect(url_for('paginate'))

    return render_template('interfaces/Research.html', title='Research', form=form)
    #else:
        #return redirect(url_for('index'))


@app.route('/feedback/', methods=['GET', 'POST'])  # routing logic, page needs content
@login_required
def feedback():
    g.user = current_user
    if g.user.s1_background is not False:
        form = FeedbackForm(request.form)
        if form.validate_on_submit():
            survey = Feedback()
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)

            g.user.s1 = True
            g.user.lastSeen = date.today()
            db.session.commit()
            return redirect(url_for('feedback_response'))

        return render_template('interfaces/Feedback.html', title='Feedback', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/testingResultCorrect/', methods=['GET', 'POST'])
@login_required
def testingResultCorrect():
    form = Testing(request.form)
    return render_template('interfaces/TestingResultCorrect.html', title='Great Work!', form=form)

@app.route('/testingResultIncorrect/', methods=['GET', 'POST'])
@login_required
def testingResultIncorrect():
    form = Testing(request.form)
  
    return render_template('interfaces/TestingResultIncorrect.html', title='Good try...', form=form)


@app.route('/training/', methods=['GET', 'POST'])
@login_required
def training():
    #g.user = current_user
    form = TrainingForm(request.form)
    if form.confident.data == 'Y':  # fixes issue of going to paginate on yes or no
        return redirect(url_for('testing'))
    elif form.confident.data == 'N':
        return redirect(url_for('research'))  # send to reserach if not ready for reviews
 

    return render_template('interfaces/training.html', title='Training', form=form)



@app.route('/testing/', methods=['GET', 'POST'])
@login_required
def testing():
    g.user = current_user
    #what did this line do?
    #if g.user.s2 is not False and g.user.s3 is False:
    form = TestingForm(request.form)
    if form.opinion.data == 'G':  # fixes issue of going to paginate on yes or no
        return redirect(url_for('testingResultCorrect'))
    elif form.opinion.data == 'F':
        return redirect(url_for('testingResultIncorrect'))  # send to reserach if not ready for reviews
    return render_template('interfaces/testing.html', title='What is AI Spam Spotting?', form=form)
    #below is made unreachable was it important?
    if form.validate_on_submit():
        survey = Testing()
        form.populate_obj(survey)
        survey.user = g.user
        db.session.add(survey)

        g.user.s2 = True
        g.user.lastSeen = date.today()
        db.session.commit()
        logout_user()
            # return redirect(url_for('logouthtml'))
       #return redirect(url_for('testing'))

        return render_template('interfaces/testing.html', title='What is AI Spam Spotting?', form=form)
    else:
        return redirect(url_for('index'))


@app.route('/feedback_response', methods=['GET', 'POST'])
@login_required
def feedback_response():
    if g.user.s1_background is not False:
        return render_template('./feedback_response.html', title='Response Recorded')
    else:
        return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                               (query.statement, query.parameters, query.duration, query.context))
    return response


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error))


# Route for pagination of review data. can GET or POST to a new page
@app.route('/paginate/', methods=['GET', 'POST'])  # paginate work for reviews
def paginate():
    # page = request.args.get('page', 1, type=int)
    # all_data = [{'username': 'Pang', 'site': 'stackoverflow.com'}, {'username': 'Judy', 'site': 'judy.com'}]
    # each_data = all_data.paginate(page, 1, False)
    # return render_template('settings.html', all_data=all_data)

    # def get_users(offset=0, per_page=10):
    # return users[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    # values from yelp
    # indexing was from 1 so added dummy row to fix page20 bug
    pagination_usrFeature = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.995024875621890, 0.08955223880597019, 0.9950248756218906, 0.9950248756218906, 0.004975124378109453,
         0.004975124378109453],

        [0.9950248756218906, 0.08955223880597019, 0.9950248756218906, 0.9502487562189055, 0.04975124378109453,
         0.004975124378109453],

        [0.9950248756218906, 0.08955223880597019, 0.9950248756218906, 0.9203980099502488, 0.07960199004975124,
         0.004975124378109453],

        [0.9950248756218906, 0.9651741293532339, 0.05472636815920395, 0.12935323383084574, 0.8805970149253731,
         0.18407960199004975],

        [0.736318407960199, 0.8109452736318408, 0.22388059701492535, 0.32835820895522383, 0.7064676616915423,
         0.9104477611940298],

        [0.5024875621890548, 0.23383084577114432, 0.791044776119403, 0.8656716417910448, 0.2835820895522388,
         0.9552238805970149],

        [0.5024875621890548, 0.7810945273631841, 0.19402985074626866, 0.1691542288557214, 0.9253731343283582,
         0.7810945273631841],

        [0.9950248756218906, 0.10447761194029848, 0.8258706467661692, 0.7711442786069651, 0.14925373134328357,
         0.22885572139303484],

        [0.5024875621890548, 0.2736318407960199, 0.7711442786069651, 0.8009950248756219, 0.32338308457711445,
         0.8009950248756219],

        [0.736318407960199, 0.7512437810945274, 0.5522388059701493, 0.6218905472636815, 0.582089552238806,
         0.3482587064676617],

        [0.9950248756218906, 0.6119402985074627, 0.4328358208955224, 0.28358208955223885, 0.6666666666666666,
         0.1890547263681592],

        [0.353238308457711, 0.2786069651741293, 0.5970149253731343, 0.5422885572139303, 0.39800995024875624,
         0.9850746268656716],

        [0.3532338308457711, 0.5323383084577115, 0.5024875621890548, 0.5472636815920398, 0.6069651741293532,
         0.8059701492537313],

        [0.3532338308457711, 0.154228855721393, 0.7014925373134329, 0.5323383084577115, 0.24378109452736318,
         0.9502487562189055],

        [0.3532338308457711, 0.1840796019900498, 0.8109452736318408, 0.7960199004975125, 0.263681592039801,
         0.44776119402985076],

        [0.3532338308457711, 0.42288557213930345, 0.43781094527363185, 0.2885572139303483, 0.4079601990049751,
         0.945273631840796],

        [0.3532338308457711, 0.5621890547263682, 0.48756218905472637, 0.5373134328358209, 0.6169154228855721,
         0.47761194029850745],

        [0.12437810945273631, 0.592039800995025, 0.4029850746268657, 0.3084577114427861, 0.736318407960199,
         0.5671641791044776],

        [0.06467661691542292, 0.4577114427860697, 0.5174129353233831, 0.6567164179104478, 0.5472636815920398,
         0.3333333333333333],

        [0.736318407960199, 0.29850746268656714, 0.263681592039801, 0.39303482587064675, 0.31343283582089554,
         0.3383084577114428]]
    avg_prodFeature = [[0.9395447007387306, 0.5286365790097131, 0.5960991064577608],
                       [0.2982059399969847, 0.5426735370765223, 0.5025370659142101],
                       [0.8386853610734207, 0.4411573086946222, 0.5064231083389026],
                       [0.7526006331976481, 0.44853115375503433, 0.4984530085888963],
                       [0.1484999246193276, 0.5706289978678039, 0.5013242246479048],
                       [0.09844715814865074, 0.570540156361052, 0.49303235068438905]]

    values = [10, 9, 8, 7, 6, 4, 7, 8]
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    pagination = Pagination(page=page, per_page=1, total=20,
                            css_framework='bootstrap4')
    return render_template('settings.html',
                           users=pagination_usrFeature,
                           avg_prod=avg_prodFeature,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           values=values,
                           labels=labels
                           )

# start of new code
@app.route("/analysis")
def analysis():
    return render_template("my_main.html")

@app.route("/Success/<input>")
def Updated(input):
    test=scrapping.Scrapping(input)
    test.setLink("https://www.newegg.ca/gigabyte-geforce-rtx-3080-ti-gv-n308tgaming-oc-12gd/p/N82E16814932436?Description=3080&cm_re=3080-_-14-932-436-_-Product")
    test.scrap(test.getLink())
    product=test.getProduct()
    price=test.getPrice()
    review=test.getReview()
    hyper=test.getLink()
    desc=test.getDescription()

    return render_template("my_display.html",link_product=hyper,product=product
    ,price=price,review=review,description=desc)

@app.route('/get_Input',methods=['POST','GET'])
def get_Input():
    if request.method== 'POST':
        product=request.form["Product"]
        return redirect(url_for("Updated",input=product))
    else:
        product=request.args.get('Product')
        return redirect(url_for("Updated",input=product))