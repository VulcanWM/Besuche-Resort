import pymongo
import dns
import json
import os
import random
from flask import session
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
mainclient = pymongo.MongoClient(os.getenv("clientm"))
usersdb = mainclient.Users
profilescol = usersdb.Users
cooldowndb = mainclient.Cooldown
cooldowncol = cooldowndb.Cooldown
notifsdb = mainclient.Notifications
notifscol = notifsdb.Notifications

def addcookie(key, value):
  session[key] = value

def delcookie(keyname):
  session.clear()

def getcookie(key):
  try:
    if (x := session.get(key)):
      return x
    else:
      return False
  except:
    return False

def makeaccount(username, password):
  passhash = generate_password_hash(password)
  document = [{
    "Username": username,
    "Password": passhash,
    "Money": 5000,
    "Bank": 100,
    "Bank-Space": 100,
    "XP": 0,
    "Health": 100,
    "Items": {}
  }]
  profilescol.insert_many(document)

def gethashpass(username):
  myquery = { "Username": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return x['Password']
  return False

def getuser(username):
  myquery = { "Username": username }
  mydoc = profilescol.find(myquery)
  for x in mydoc:
    return x
  return False

def getusercddoc(username):
  myquery = { "Username": username }
  mydoc = cooldowncol.find(myquery)
  for x in mydoc:
    return x
  return False

def getusercd(username):
  check = {}
  myquery = { "Username": username }
  mydoc = cooldowncol.find(myquery)
  for x in mydoc:
    check['hello'] = True
    user = x
  if "hello" not in check:
    return False
  cd = []
  things = ["XP", "Daily"]
  if user['XP'] == None:
    cd.append("Ready")
  else:
    thetime = user['XP']
    a = datetime.datetime(int(thetime.split()[0]), int(thetime.split()[1]), int(thetime.split()[2]), int(thetime.split()[3]), int(thetime.split()[4]), int(thetime.split()[5]))
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    b = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    seconds = (b-a).total_seconds()
    if seconds > 60:
      cd.append("Ready")
    else:
      cd.append(f"{str(600 - seconds)} seconds left")
  if user['Daily'] == None:
    cd.append("Ready")
  else:
    thetime = user['Daily']
    a = datetime.datetime(int(thetime.split()[0]), int(thetime.split()[1]), int(thetime.split()[2]), int(thetime.split()[3]), int(thetime.split()[4]), int(thetime.split()[5]))
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    b = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
    seconds = (b-a).total_seconds()
    if seconds > 86400:
      cd.append("Ready")
    else:
      cd.append(f"{str(84000 - seconds)} seconds left")
  return cd

def allusers():
  users = []
  for user in profilescol.find():
    users.append(user['Username'].lower())
  return users

def getitem(item, type):
  with open(f'items/{type}.json') as json_file:
    data = json.load(json_file)
  json_file.close()
  for itemname in data:
    if itemname['Item'].lower() == item.lower():
      return itemname

def buycafeitem(username, item):
  user = getuser(username)
  user2 = user
  money = user2['Money']
  xp = user2['Health']
  itemstats = getitem(item, "cafe")
  if int(user['Money']) < int(itemstats['Cost']):
    return "You don't have enough money!"
  money = int(money) - itemstats['Cost']
  xp = int(xp) + itemstats['XP']
  if xp > 99:
    return "If you buy that you will have more than 100 Health and you can't have that!"
  del user2['Money']
  del user2['Health']
  user2['Money'] = money
  user2['Health'] = xp
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def buyrestaurantitem(username, item):
  user = getuser(username)
  user2 = user
  money = user2['Money']
  xp = user2['Health']
  itemstats = getitem(item, "restaurant")
  if int(user['Money']) < int(itemstats['Cost']):
    return "You don't have enough money!"
  money = int(money) - itemstats['Cost']
  xp = int(xp) + itemstats['XP']
  if xp > 99:
    return "If you buy that you will have more than 100 Health and you can't have that!"
  del user2['Money']
  del user2['Health']
  user2['Money'] = money
  user2['Health'] = xp
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def buybaritem(username, item):
  user = getuser(username)
  user2 = user
  money = user2['Money']
  xp = user2['Health']
  itemstats = getitem(item, "bar")
  if int(user['Money']) < int(itemstats['Cost']):
    return "You don't have enough money!"
  money = int(money) - itemstats['Cost']
  xp = int(xp) + itemstats['XP']
  if xp > 99:
    return "If you buy that you will have more than 100 Health and you can't have that!"
  del user2['Money']
  del user2['Health']
  user2['Money'] = money
  user2['Health'] = xp
  profilescol.delete_one({"Username": username})
  profilescol.insert_many([user2])
  return True

def rolldice(username, number, bet):
  bet = int(bet)
  if int(bet) < 10:
    return "You have to bet more than ₹10!"
  if int(bet) > 10000:
    return "You have to bet less than ₹10000!"
  if float(getuser(username)['Money']) < float(bet):
    return f"You don't have ₹{str(bet)}!"
  dice = random.randint(1,6)
  if int(dice) == int(number):
    user = getuser(username)
    user2 = user
    money = user2['Money']
    del user2['Money']
    user2['Money'] = int(money) + (int(bet) * 6)
    delete = {"_id": user['_id']}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"The dice rolled {str(dice)}! You won ₹{str(int(bet) * 6)}!"
  else:
    user = getuser(username)
    user2 = user
    money = user2['Money']
    del user2['Money']
    user2['Money'] = int(money) - int(bet)
    delete = {"_id": user['_id']}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"The dice rolled {str(dice)}! You lost ₹{str(bet)}!"

def flipcoin(username, side, bet):
  bet = int(bet)
  if int(bet) < 10:
    return "You have to bet more than ₹10!"
  if int(bet) > 2500:
    return "You have to bet less than ₹2500!"
  if float(getuser(username)['Money']) < float(bet):
    return f"You don't have ₹{str(bet)}!"
  coin = random.choice(['heads', 'tails'])
  if side == coin:
    user = getuser(username)
    user2 = user
    money = user2['Money']
    del user2['Money']
    user2['Money'] = int(float) + int(bet)
    delete = {"_id": user['_id']}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"The coin flipped {coin}! You won ₹{str(bet)}!"
  else:
    user = getuser(username)
    user2 = user
    money = user2['Money']
    del user2['Money']
    user2['Money'] = int(money) - int(bet)
    delete = {"_id": user['_id']}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"The coin flipped {str(coin)}! You lost ₹{str(bet)}!"

def cupgame(username, number, bet):
  bet = int(bet)
  if int(bet) < 10:
    return "You have to bet more than ₹10!"
  if int(bet) > 5000:
    return "You have to bet less than ₹5000!"
  if float(getuser(username)['Money']) < float(bet):
    return f"You don't have ₹{str(bet)}!"
  cup = random.randint(1,3)
  if int(number) == int(cup):
    user = getuser(username)
    user2 = user
    money = user2['Money']
    del user2['Money']
    user2['Money'] = int(money) + int(bet * 3)
    delete = {"_id": user['_id']}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"The ball was in cup number {str(cup)}! You won ₹{str(int(bet) * 3)}!"
  else:
    user = getuser(username)
    user2 = user
    money = user2['Money']
    del user2['Money']
    user2['Money'] = int(money) - int(bet)
    delete = {"_id": user['_id']}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"The ball was in cup number {str(cup)}! You lost ₹{str(bet)}!"

def getxp(username):
  usercd = getusercd(username)
  if usercd == False:
    user = getuser(username)
    user2 = user
    xp = user2['XP']
    health = user2['Health']
    increase = random.randint(1,5)
    decrease = random.randint(1,5)
    del user2['XP']
    del user2['Health']
    newxp = int(xp) + increase
    newhealth = int(health) - decrease
    user2['XP'] = newxp
    user2['Health'] = newhealth
    delete = {"Username": username}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    thetime = year + " " + month + " " + day + " " + hour + " " + minute + " " + second
    user2 = {"Username": username,"XP": thetime, "Daily": None}
    cooldowncol.insert_many([user2])
    return True
  if usercd[0] == "Ready":
    user = getuser(username)
    user2 = user
    xp = user2['XP']
    health = user2['Health']
    increase = random.randint(1,5)
    decrease = random.randint(1,5)
    del user2['XP']
    del user2['Health']
    newxp = int(xp) + increase
    newhealth = int(health) - decrease
    user2['XP'] = newxp
    user2['Health'] = newhealth
    delete = {"Username": username}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    current = datetime.datetime.utcnow()
    year = str(current).split("-")[0]
    month = str(current).split("-")[1]
    daypart = str(current).split("-")[2]
    day = str(daypart).split()[0]
    something1 = str(current).split()[1]
    something = something1.split(".")[0]
    hour = something.split(":")[0]
    minute = something.split(":")[1]
    second = something.split(":")[2]
    thetime = year + " " + month + " " + day + " " + hour + " " + minute + " " + second
    user2 = getusercddoc(username)
    del user2['XP']
    user2['XP'] = thetime
    delete = {"Username": username}
    cooldowncol.delete_one(delete)
    cooldowncol.insert_many([user2])
    return True
  else:
    return False

def getnotifs(username):
  myquery = { "Username": username }
  mydoc = notifscol.find(myquery)
  notifs = []
  for x in mydoc:
    notifs.append(x)
  return notifs

def addnotif(username, notif):
  notif = {"Username": username, "Notification": notif, "Seen": False}
  notifscol.insert_many([notif])
  return True

def clearnotifs(username):
  notifs = getnotifs(username)
  for notif in notifs:
    delete = {"_id": notif['_id']}
    notifscol.delete_one(delete)
  return True

def allseen(username):
  notifs = getnotifs(username)
  myquery = { "Username": username }
  newvalues = { "$set": { "Seen": True } }
  notifscol.update_many(myquery, newvalues)
  return True

def spawnitem(username, place):
  number = random.randint(1,1000)
  print("Number: " + str(number))
  if number > 0 and number < 51:
    amount = random.randint(1,1000)
    user = getuser(username)
    money = user['Money']
    money = int(money) + amount
    myquery = { "Username": username }
    newvalues = { "$set": { "Money": money } }
    profilescol.update_many(myquery, newvalues)
    return f"You went to the {place} and somehow got yourself ₹{str(amount)}!"
  elif number == 69:
    user = getuser(username)
    user2 = user
    if "bank-note" in user['Items']:
      amount = user['Items']['bank-note']
      something = random.randint(1,5)
      same = something
      amount = int(amount) + something
      del user2['Items']['bank-note']
    else:
      amount = random.randint(1,5)
      same = amount
    user2['Items']['bank-note'] = amount
    delete = {"Username": username}
    profilescol.delete_one(delete)
    profilescol.insert_many([user2])
    return f"You went to the {place} and somehow got yourself {same} bank notes!"
  else:
    return False