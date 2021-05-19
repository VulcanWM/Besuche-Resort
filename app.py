from flask import Flask, render_template, request, redirect, flash
import os
from functions import getcookie, allusers, makeaccount, addcookie, getuser, gethashpass, delcookie
from werkzeug.security import check_password_hash
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route('/')
def home():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    return render_template("main.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
  if request.method == 'POST':
    if getcookie("User") != False:
      return render_template("error.html", error="You have already logged in!")
    username = request.form['username']
    if username.lower() in allusers():
      return render_template("error.html", error="A user already has this username! Try another one.")
    password = request.form['password']
    passworda = request.form['passwordagain']
    if password != passworda:
      return render_template("error.html", error="The two passwords don't match!")
    makeaccount(username, password)
    addcookie("User", username)
    return redirect("/")

@app.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    if getcookie("User") != False:
      return render_template("error.html", error="You have already logged in!")
    username = request.form['username']
    if getuser(username) == False:
      return render_template("error.html", error="That is not a username!")
    password = request.form['password']
    if check_password_hash(gethashpass(username), password) == False:
      return render_template("error.html", error="Wrong password!")
    addcookie("User", username)
    return redirect("/")

@app.route("/beach")
def beach():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    return render_template("beach.html")

@app.route("/logout")
def logout():
  delcookie("User")
  return redirect("/")