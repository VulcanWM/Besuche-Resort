from flask import Flask, render_template, request, redirect
import json
import os
from functions import getcookie, allusers, makeaccount, addcookie, getuser, gethashpass, delcookie, buycafeitem, getitem, buyrestaurantitem, buybaritem
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

@app.route("/cafe")
def cafe():
  if getcookie("User") == False:
    return render_template("login.html")
  with open('items/cafe.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Cafe", nocap="cafe")

@app.route("/buycafeitem/<item>")
def buycafeitemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  func = buycafeitem(getcookie("User"), item)
  if func == True:
    money = str(getitem(item, "cafe")['Cost'])
    xp = str(getitem(item, "cafe")['XP'])
    return f"You bought {item} with ₹{money}, ate it and gained {xp} XP!"
  else:
    return render_template("error.html", error=func)

@app.route("/restaurant")
def restaurant():
  if getcookie("User") == False:
    return render_template("login.html")
  with open('items/restaurant.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Restaurant", nocap="restaurant")

@app.route("/buyrestaurantitem/<item>")
def buyrestaurantitemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  func = buyrestaurantitem(getcookie("User"), item)
  if func == True:
    money = str(getitem(item, "restaurant")['Cost'])
    xp = str(getitem(item, "restaurant")['XP'])
    return f"You bought {item} with ₹{money}, ate it and gained {xp} XP!"
  else:
    return render_template("error.html", error=func)

@app.route("/bar")
def bar():
  if getcookie("User") == False:
    return render_template("login.html")
  with open('items/bar.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Bar", nocap="bar")

@app.route("/buybaritem/<item>")
def buybaritemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  func = buybaritem(getcookie("User"), item)
  if func == True:
    money = str(getitem(item, "bar")['Cost'])
    xp = str(getitem(item, "bar")['XP'])
    return f"You bought {item} with ₹{money}, drank it and gained {xp} XP!"
  else:
    return render_template("error.html", error=func)

@app.route("/logout")
def logout():
  delcookie("User")
  return redirect("/")

@app.route("/pool")
def pool():
  return render_template("pool.html")