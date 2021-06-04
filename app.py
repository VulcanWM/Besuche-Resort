from flask import Flask, render_template, request, redirect
import pymongo
import json
import os
mainclient = pymongo.MongoClient(os.getenv("clientm"))
usersdb = mainclient.Users
profilescol = usersdb.Users
from functions import getcookie, allusers, makeaccount, addcookie, getuser, gethashpass, buycafeitem, getitem, buyrestaurantitem, buybaritem, cupgame, flipcoin, rolldice, getxp, getnotifs, clearnotifs, allseen, spawnitem, buyshopitem, useitem, getitemused, rob, moneylb, banklb, bankspacelb, dailyfunc, withdraw, deposit
from string import printable
from functions import delcookie
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
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    return render_template("index.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
  if request.method == 'POST':
    if getcookie("User") != False:
      return render_template("error.html", error="You have already logged in!")
    username = request.form['username']
    if len(username) > 25:
      return render_template("error.html", error="Your username cannot have more than 25 letters!")
    if len(username) < 2:
      return render_template("error.html", error="You have to have more than 2 letters in your username!")
    if set(username).difference(printable):
      return render_template("error.html", error="Your username cannot contain any special characters!")
    if username.lower() in allusers():
      return render_template("error.html", error="A user already has this username! Try another one.")
    password = request.form['password']
    passworda = request.form['passwordagain']
    if password != passworda:
      return render_template("error.html", error="The two passwords don't match!")
    if len(password) > 25:
      return render_template("error.html", error="Your password cannot have more than 25 letters!")
    if len(password) < 2:
      return render_template("error.html", error="You have to have more than 2 letters in your password!")
    if set(password).difference(printable):
      return render_template("error.html", error="Your password cannot contain any special characters!")
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
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "beach")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("beach.html")

@app.route("/cafe")
def cafe():
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  with open('items/cafe.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Cafe", nocap="cafe")

@app.route("/buycafeitem/<item>")
def buycafeitemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
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
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  with open('items/restaurant.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Restaurant", nocap="restaurant")

@app.route("/buyrestaurantitem/<item>")
def buyrestaurantitemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
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
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  with open('items/bar.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Bar", nocap="bar")

@app.route("/buybaritem/<item>")
def buybaritemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  func = buybaritem(getcookie("User"), item)
  if func == True:
    money = str(getitem(item, "bar")['Cost'])
    xp = str(getitem(item, "bar")['XP'])
    return render_template("success.html", success=f"You bought {item} with ₹{money}, drank it and gained {xp} XP!")
  else:
    return render_template("error.html", error=func)

@app.route("/shop")
def shop():
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  with open('items/shop.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  return render_template("cafe.html", items=data, cap="Shop", nocap="shop", noxp=True)

@app.route("/buyshopitem/<item>")
def buyshopitemfunc(item):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  func = buyshopitem(getcookie("User"), item)
  if func == True:
    money = str(getitem(item, "shop")['Cost'])
    return render_template("success.html", success=f"You bought {item} with ₹{money}!")
  else:
    return render_template("error.html", error=func)

@app.route("/profile")
def profile():
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  user = getuser(getcookie("User"))
  items = user['Items']
  activeitems = getitemused(getcookie("User"))
  return render_template("profile.html", user=user, items=items, activeitems=activeitems)

@app.route("/outdoorpool")
def outdoorpool():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
     return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "outdoor swimming pool")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("outdoorpool.html")
  
@app.route("/disco")
def disco():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "disco")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("disco.html")

@app.route("/indoorpool")
def indoorpool():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "indoor swimming pool")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("indoorpool.html")

@app.route("/cinema")
def cinema():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "cinema")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("cinema.html")

@app.route("/casino")
def casino():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "casino")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("gambling.html")

@app.route("/rolldice", methods=['POST', 'GET'])
def rollapp():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
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
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
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
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
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

@app.route("/use<itemname>")
def useanitem(itemname):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  if getuser(getcookie("User"))['Health'] < 1:
    return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
  user = getuser(getcookie("User"))
  items = user['Items']
  for item in items.keys():
    if item.lower() == itemname.lower():
      amount = items[item]
      if 1 > amount:
        return render_template("error.html", error=f"You don't have any {item}s")
      if item.lower() == "bank-note":
        increase = 0
        for i in range(int(1)):
          increase = int(increase) + random.randint(5000,10000)
        bank = user['Bank-Space']
        banknew = int(bank) + int(increase)
        user2 = user
        del user2['Bank-Space']
        itemamount = int(amount) - int(1)
        del user2['Items'][item]
        user2['Items'][item] = int(itemamount)
        user2['Bank-Space'] = banknew
        delete = {"Username": getcookie("User")}
        profilescol.delete_one(delete)
        profilescol.insert_many([user])
        return render_template("success.html", success=f"You used 1 banknote and got {increase} more bank space!")
      else:
        func = useitem(getcookie("User"), itemname)
        if func == True:
          return render_template("success.html", success=f"You used an {item}!")
        else:
          return render_template("error.html", error=func)

@app.route("/notifs")
def notifs():
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  notifs = getnotifs(getcookie("User"))
  allseen(getcookie("User"))
  return render_template("notifs.html", notifs=notifs)

@app.route("/clearnotifs")
def clearnotifsapp():
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  clearnotifs(getcookie("User"))
  return redirect("/notifs")

@app.route("/toddlersarea")
def toddlersarea():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    if getuser(getcookie("User"))['Health'] < 1:
      return render_template("error.html", error="You don't have any health! Go to the cafe, restauant or bar to get some.")
    getxp(getcookie("User"))
    spawn = spawnitem(getcookie("User"), "toddler's area")
    if spawn != False:
      return render_template("success.html", success=spawn)
    return render_template("toddler.html")

@app.route("/rob")
def robapp():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    return render_template("rob.html")

@app.route("/rob", methods=['POST', 'GET'])
def robfunc():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    username = request.form['username']
    return redirect(f'/robfunc/{username}')

@app.route("/robfunc/<username>")
def robfuncapp(username):
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  func = rob(username, getcookie("User"))
  if func.startswith("Yay") == True:
    return render_template("success.html", success=func)
  else:
    return render_template("error.html", error=func)

@app.route("/leaderboards")
def leaderboards():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    return render_template("leaderboard.html", users=moneylb(getcookie("User")), bank=banklb(), bankspace=bankspacelb())

@app.route("/rules")
def rules():
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  return render_template("rules.html")

@app.route("/daily")
def daily():
  if getcookie("User") == False:
    return render_template("login.html")
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  func = dailyfunc(getcookie("User"))
  if func.startswith("Stop") == True:
    return render_template("error.html", error=func)
  else:
    return render_template("success.html", success=func)

@app.route("/withdraw")
def withdrawapp():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    return render_template("withdraw.html")

@app.route("/withdraw", methods=['POST', 'GET'])
def withdrawfunc():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    amount = int(request.form['amount'])
    func = withdraw(getcookie("User"), amount)
    if isinstance(func, int) == True:
      return render_template("success.html", success=f"You withdrawed ₹{str(amount)} from your bank account!")
    else:
      return render_template("error.html", error=func)

@app.route("/deposit")
def depositapp():
  if getcookie("User") == False:
    return render_template("login.html")
  else:
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    return render_template("deposit.html")

@app.route("/deposit", methods=['POST', 'GET'])
def depositfunc():
  if request.method == 'POST':
    if getcookie("User") == False:
      return render_template("login.html")
    if getuser(getcookie("User")) == False:
      delcookie("hello")
      return redirect("/")
    amount = int(request.form['amount'])
    func = deposit(getcookie("User"), amount)
    if isinstance(func, int) == True:
      return render_template("success.html", success=f"You deposited ₹{str(amount)} from your bank account!")
    else:
      return render_template("error.html", error=func)

@app.route("/guide")
def guide():
  if getuser(getcookie("User")) == False:
    delcookie("hello")
    return redirect("/")
  return render_template("guide.html")

# @app.route("/logout")
# def logout():
#   delcookie("User")
#   return redirect("/")