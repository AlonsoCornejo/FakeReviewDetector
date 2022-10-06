#from itertools import product
#from Demo.scrapping import Scrapping
from flask import Flask, redirect, url_for, render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import scrapping

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                #primary key that identifies the product
    image_file = db.Column(db.Text, nullable = True, default='default.jpg')     #store the string path to image of product to use in html later, can be empty, needs to be hashed?
    descript = db.Column(db.Text, nullable = True)                              #store the product description, can be empty
    product_url = db.Column(db.Text, unique = True, nullable = False)           #store the product url, cannot be empty since we need a url to the product
    
    

@app.route("/")
def Home():
    return render_template("main.html")

@app.route("/Success/<input>")
def Updated(input):
    test=scrapping.Scrapping()
    test_t=test.getName()
    user=str(test_t)
    return render_template("display.html",product_name=input,person=user)

@app.route('/get_Input',methods=['POST','GET'])
def get_Input():
    if request.method== 'POST':
        product=request.form["Product"]
        return redirect(url_for("Updated",input=product))
    else:
        product=request.args.get('Product')
        return redirect(url_for("Updated",input=product))

if __name__=="__main__":
    app.run(debug=True)
    
