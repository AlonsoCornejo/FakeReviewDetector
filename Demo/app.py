from flask import Flask, redirect, url_for, render_template

app= Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/test", methods=["POST","GET"])
def login():
    return render_template("test.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__=="__main__":
    app.run(debug=True)