import pymongo
import dns
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
    "Money": 0,
    "XP": 0,
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