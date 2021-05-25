import pymongo
import dns
import json
import os
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
mainclient = pymongo.MongoClient(os.getenv("clientm"))
usersdb = mainclient.Users
profilescol = usersdb.Users

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
    "Items": []
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