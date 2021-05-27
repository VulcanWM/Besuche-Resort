from flask import Flask, render_template, request, redirect
import pymongo
import json
import os
mainclient = pymongo.MongoClient(os.getenv("clientm"))
usersdb = mainclient.Users
profilescol = usersdb.Users
from functions import getcookie, allusers, makeaccount, addcookie, getuser, gethashpass, buycafeitem, getitem, buyrestaurantitem, buybaritem, cupgame, flipcoin, rolldice, getxp
# from functions import delcookie
import random
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
    return render_template("index.html")

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
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
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
    return render_template("success.html", success=f"You bought {item} with ₹{money}, ate it and gained {xp} XP!")
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
    return render_template("success.html", success=f"You bought {item} with ₹{money}, ate it and gained {xp} XP!")
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
    return render_template("success.html", success=f"You bought {item} with ₹{money}, drank it and gained {xp} XP!")
  else:
    return render_template("error.html", error=func)

@app.route("/profile")
def profile():
  if getcookie("User") == False:
    return render_template("login.html")
  user = getuser(getcookie("User"))
  items = user['Items']
  return render_template("profile.html", user=user, items=items)

@app.route("/outdoorpool")
def outdoorpool():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User"))['Health'] < 1:
     return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    return render_template("outdoorpool.html")
  
@app.route("/disco")
def disco():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    return render_template("disco.html")

@app.route("/indoorpool")
def indoorpool():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    return render_template("indoorpool.html")

@app.route("/cinema")
def cinema():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    return render_template("cinema.html")

@app.route("/casino")
def casino():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    return render_template("gambling.html")

@app.route("/rolldice", methods=['POST', 'GET'])
def rollapp():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    number = request.form['number']
    bet = request.form['bet']
    func = rolldice(getcookie("User"), number, bet)
    if func.startswith("You "):
      return render_template("error.html", error=func)
    if "lost" in func:
      return render_template("error.html", error=func)
    if "won" in func:
      return render_template("success.html", success=func)

@app.route("/flipcoin", methods=['POST', 'GET'])
def flipapp():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    side = request.form['side']
    bet = request.form['bet']
    func = flipcoin(getcookie("User"), side, bet)
    if func.startswith("You "):
      return render_template("error.html", error=func)
    if "lost" in func:
      return render_template("error.html", error=func)
    if "won" in func:
      return render_template("success.html", success=func)

@app.route("/cupgame", methods=['POST', 'GET'])
def cupapp():
  if request.method == "POST":
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    number = request.form['number']
    bet = request.form['bet']
    func = cupgame(getcookie("User"), number, bet)
    if func.startswith("You "):
      return render_template("error.html", error=func)
    if "lost" in func:
      return render_template("error.html", error=func)
    if "won" in func:
      return render_template("success.html", success=func)

@app.route("/use<itemname>/<number>")
def usebanknote(itemname, number):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User"))['Health'] < 1:
    return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
  getxp(getcookie("User"))
  user = getuser(getcookie("User"))
  items = user['Items']
  for item in items.keys():
    if item.lower() == itemname.lower():
      amount = items[item]
      if int(number) > amount:
        return render_template("error.html", error=f"You don't have {number} {item}s")
      if item.lower() == "banknote":
        increase = 0
        for i in range(int(number)):
          increase = int(increase) + random.randint(5000,10000)
        bank = user['Bank-Space']
        banknew = int(bank) + int(increase)
        user2 = user
        del user2['Bank-Space']
        itemamount = int(amount) - int(number)
        del user2['Items'][item]
        user2['Items'][item] = int(itemamount)
        user2['Bank-Space'] = banknew
        delete = {"Username": getcookie("User")}
        profilescol.delete_one(delete)
        profilescol.insert_many([user])
        return render_template("success.html", success=f"You used {number} banknote(s) and got {increase} more bank space!")

# @app.route("/logout")
# def logout():
#   delcookie("User")
#   return redirect("/")