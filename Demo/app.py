from flask import Flask, redirect, url_for, render_template,request
from werkzeug.utils import redirect

app= Flask(__name__)

@app.route("/")
def Home():
    return render_template("main.html")

@app.route("/Success/<input>")
def Updated(input):
    return 'You inserted: %s' % input

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
    
