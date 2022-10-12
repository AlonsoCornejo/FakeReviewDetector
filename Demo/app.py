#from itertools import product
#from Demo.scrapping import Scrapping
from pydoc import describe
from flask import Flask, redirect, url_for, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.utils import redirect
import scrapping

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Product(db.Model):
    _tablename_ = "product"
    id = db.Column(db.Integer, primary_key=True)                                    #primary key that identifies the product
    image_file = db.Column(db.Text, nullable = True, default='default.jpg')         #store the string path to image of product to use in html later, can be empty, needs to be hashed?
    descript = db.Column(db.Text, nullable = True)                                  #store the product description, can be empty
    prod_url = db.Column(db.Text, unique = True, nullable = False)                  #store the product url, cannot be empty since we need a url to the product
    reviews = db.relationship('Review', backref='original_review', lazy=True)
    
    def __repr__(self):                                                             #dunder method or magic method to represent database when its printed out
        return f"Product('{self.image_file}','{self.descript}','{self.prod_url}')"

class Review(db.Model):
    _tablename_ = "review"
    id = db.Column(db.Integer, primary_key=True)                                    #primary key that identifies the product
    prod_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)    #store which product id this review is associated with, using it as a foreign key
    chart1 = db.Column(db.Text, nullable = False)                                   #store the jpg of the chart associated with this review based on algorithm result
    alg1 = db.Column(db.Text, nullable = False)                                     #store result of first algorithm
    chart2 = db.Column(db.Text, nullable = False)                                   #store the jpg of the chart associated with this review based on algorithm result
    alg2 = db.Column(db.Text, nullable = False)                                     #store result of first algorithm
    
    def __repr__(self):                                                             #dunder method or magic method to represent database when its printed out
        return f"Product('{self.prod_id}','{self.chart1}','{self.alg1}','{self.chart2}','{self.alg2}')"

    
@app.route("/")
def Home():
    return render_template("main.html")

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

    return render_template("display.html",link_product=hyper,product=product
    ,price=price,review=review,description=desc)

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
    
