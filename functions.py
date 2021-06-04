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
cooldowncol = usersdb.Cooldown
notifscol = usersdb.Notifications
itemsdb = mainclient.Items

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
    "Items": {},
    "Streak": 0
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
    if x.get("Deleted", None) == None:
      return x
    return False
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
    cd.append(["Ready", None])
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
      cd.append(["Ready", str(seconds)])
    else:
      cd.append([f"{str(84000 - seconds)} seconds left"])
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
    user2['Money'] = int(money) + int(bet)
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

def buyshopitem(username, item):
  if item not in ['padlock', 'camera', 'fake-id', 'robbers-wishlist']:
    return "This is not an item in the shop!"
  user = getuser(username)
  user2 = user
  money = user2['Money']
  itemstats = getitem(item, "shop")
  if int(user['Money']) < int(itemstats['Cost']):
    return "You don't have enough money!"
  if item in user['Items']:
    amount = user['Items'][item] + 1
    del user2['Items'][item]
    user2['Items'][item] = amount
  else:
    amount = 1
    user2['Items'][item] = amount
  del user2['Money']
  user2['Money'] = int(money) - int(itemstats['Cost'])
  delete = {"Username": username}
  profilescol.delete_one(delete)
  profilescol.insert_many([user2])
  return True

def getitemused(username):
  used = {"padlock": False, "camera": False, "fake-id": False, "robbers-wishlist": False}
  padlockcol = itemsdb['padlock']
  myquery = { "Username": username }
  mydoc = padlockcol.find(myquery)
  for x in mydoc:
    del used['padlock']
    used['padlock'] = True
  cameracol = itemsdb['camera']
  myquery = { "Username": username }
  mydoc = cameracol.find(myquery)
  for x in mydoc:
    del used['camera']
    used['camera'] = True
  fakeidcol = itemsdb['fake-id']
  myquery = { "Username": username }
  mydoc = fakeidcol.find(myquery)
  for x in mydoc:
    del used['fake-id']
    used['fake-id'] = True
  wishlistcol = itemsdb['robbers-wishlist']
  myquery = { "Username": username }
  mydoc = wishlistcol.find(myquery)
  for x in mydoc:
    del used['robbers-wishlist']
    used['robbers-wishlist'] = True
  return used

def useitem(username, item):
  if item not in ['padlock', 'camera', 'fake-id', 'robbers-wishlist']:
    return "This is not an item in the shop!"
  user = getuser(username)
  used = getitemused(username)
  if used[item] != False:
    return f"You already have an active {item}"
  itemamount = user['Items'].get(item, 0)
  if itemamount < 1:
    return f"You don't have any {item}"
  itemamount = int(itemamount) - int(1)
  user2 = user
  del user2['Items'][item]
  user2['Items'][item] = int(itemamount)
  delete = {"Username": username}
  profilescol.delete_one(delete)
  profilescol.insert_many([user2])
  itemcol = itemsdb[item]
  document = [{
    "Username": username
  }]
  itemcol.insert_many(document)
  return True

def rob(username, enemy):
  if getuser(enemy)['Money'] < 200:
    return "You have to have at least ₹200 to rob someone!"
  if getuser(username)['Money'] == 0:
    return f"{username} doesn't have any money!"
  if username.lower() == enemy.lower():
    return "You cannot rob yourself!"
  if getitemused(username)['camera'] == True:
    number = random.randint(1,2)
    if number == 1:
      delete = {"Username": username}
      camcol = itemsdb['camera']
      camcol.delete_one(delete)
      money = getuser(username)['Money']
      enemymoney = getuser(enemy)['Money']
      newmoney = money + enemymoney
      myquery = { "Username": enemy }
      newvalues = { "$set": { "Money": 0 } }
      profilescol.update_many(myquery, newvalues)
      myquery = { "Username": username }
      newvalues = { "$set": { "Money": newmoney } }
      profilescol.update_many(myquery, newvalues)
      addnotif(username, f"{enemy} tried to steal from you but your camera saw what was happening and gave you all their money. Unfortunately, your camera broke!")
      return f"You tried to rob {username} but they had a camera and saw what was happening, so you had to give all your money to them!"
    else:
      money = getuser(username)['Money']
      enemymoney = getuser(enemy)['Money']
      newmoney = money + enemymoney
      myquery = { "Username": enemy }
      newvalues = { "$set": { "Money": 0 } }
      profilescol.update_many(myquery, newvalues)
      myquery = { "Username": username }
      newvalues = { "$set": { "Money": newmoney } }
      profilescol.update_many(myquery, newvalues)
      addnotif(username, f"{enemy} tried to steal from you but your camera saw what was happening and gave you all their money!")
      return f"You tried to rob {username} but they had a camera and saw what was happening, so you had to give all your money to them!"
  if getitemused(username)['padlock'] == True:
    number = random.randint(1,5)
    if number == 1:
      delete = {"Username": username}
      camcol = itemsdb['padlock']
      camcol.delete_one(delete)
      money = getuser(username)['Money']
      enemymoney = getuser(enemy)['Money']
      loss = random.randint(0, enemymoney)
      newmoney = money + loss
      enemymoneynew = enemymoney - loss
      myquery = { "Username": enemy }
      newvalues = { "$set": { "Money": enemymoneynew } }
      profilescol.update_many(myquery, newvalues)
      myquery = { "Username": username }
      newvalues = { "$set": { "Money": newmoney } }
      profilescol.update_many(myquery, newvalues)
      addnotif(username, f"{enemy} tried to steal from you but your padlock protected you and they left ₹{str(loss)}! Unfortunately, your padlock broke.")
      return f"You tried to rob {username} but they had a padlock so you had to give them ₹{str(loss)}!"
    else:
      money = getuser(username)['Money']
      enemymoney = getuser(enemy)['Money']
      loss = random.randint(0, enemymoney)
      newmoney = money + loss
      enemymoneynew = enemymoney - loss
      myquery = { "Username": enemy }
      newvalues = { "$set": { "Money": enemymoneynew } }
      profilescol.update_many(myquery, newvalues)
      myquery = { "Username": username }
      newvalues = { "$set": { "Money": newmoney } }
      profilescol.update_many(myquery, newvalues)
      addnotif(username, f"{enemy} tried to steal from you but your padlock protected you and they left ₹{str(loss)}!")
      return f"You tried to rob {username} but they had a padlock so you had to give them ₹{str(loss)}!"
  number = random.randint(1,2)
  if number == 1:
    money = getuser(username)['Money']
    enemymoney = getuser(enemy)['Money']
    loss = random.randint(0, money)
    newmoney = money - loss
    enemymoneynew = enemymoney + loss
    myquery = { "Username": enemy }
    newvalues = { "$set": { "Money": enemymoneynew } }
    profilescol.update_many(myquery, newvalues)
    myquery = { "Username": username }
    newvalues = { "$set": { "Money": newmoney } }
    profilescol.update_many(myquery, newvalues)
    addnotif(username, f"{enemy} stole ₹{str(loss)} from you!")
    return f"Yay! You stole ₹{str(loss)} from {username}!"
  else:
    money = getuser(username)['Money']
    enemymoney = getuser(enemy)['Money']
    loss = random.randint(0, enemymoney)
    newmoney = money + loss
    enemymoneynew = enemymoney - loss
    myquery = { "Username": enemy }
    newvalues = { "$set": { "Money": enemymoneynew } }
    profilescol.update_many(myquery, newvalues)
    myquery = { "Username": username }
    newvalues = { "$set": { "Money": newmoney } }
    profilescol.update_many(myquery, newvalues)
    addnotif(username, f"{enemy} tried to steal from you but someone saw them rob you so they left ₹{str(loss)}!")
    return f"You tried to rob {username} but someone saw you so you had to give them ₹{str(loss)}!"

def moneylb(username):
  users = []
  wishlist = getitemused(username)['robbers-wishlist']
  rank = 0
  for user in profilescol.find().sort("Money", -1).limit(10):
    if wishlist == False:
      if getitemused(user['Username'])['fake-id'] !=  False:
        del user['Username']
        user['Username'] = "haha this user has a fake id"
    rank = rank + 1
    user['Rank'] = rank
    users.append(user)
  return users

def banklb():
  users = []
  rank = 0
  for user in profilescol.find().sort("Bank", -1).limit(10):
    rank = rank + 1
    user['Rank'] = rank
    users.append(user)
  return users

def bankspacelb():
  users = []
  rank = 0
  for user in profilescol.find().sort("Bank-Space", -1).limit(10):
    rank = rank + 1
    user['Rank'] = rank
    users.append(user)
  return users

def dailyfunc(username):
  usercd = getusercd(username)
  if usercd[1][0] != "Ready":
    return "Stop being greedy!"
  user = getuser(username)
  thestreak = user['Streak']
  if usercd[1][1] == None or usercd[1][1] < 172800:
    streak = user['Streak']
    streak = streak + 1
    user['Streak'] = streak
  else:
    del user['Streak']
    user['Streak'] = 0
  money = user['Money']
  new = (thestreak + 1) * 500
  newmoney = new + money
  del user['Money']
  user['Money'] = newmoney
  delete = {"Username": username}
  profilescol.delete_one(delete)
  profilescol.insert_many([user])
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
  del user2['Daily']
  user2['Daily'] = thetime
  delete = {"Username": username}
  cooldowncol.delete_one(delete)
  cooldowncol.insert_many([user2])
  return f"You claimed ₹{str(new)} for your daily! Come back in 24 hours to claim another one"

def withdraw(username, amount):
  if amount > getuser(username)['Bank']:
    return f"You don't have ₹{str(amount)} in your bank!"
  if amount < 1:
    return "You have to withdraw at least ₹1!"
  user = getuser(username)
  money = user['Money']
  bank = user['Bank']
  banknew = int(bank) - int(amount)
  moneynew = int(money) + int(amount)
  del user['Money']
  user['Money'] = moneynew
  del user['Bank'] 
  user['Bank'] = banknew
  delete = {"Username": username}
  profilescol.delete_one(delete)
  profilescol.insert_many([user])
  return int(amount)

def deposit(username, amount):
  if amount > getuser(username)['Money']:
    return f"You don't have ₹{str(amount)} in your wallet!"
  if amount < 1:
    return "You have to deposit at least ₹1!"
  user = getuser(username)
  money = user['Money']
  bank = user['Bank']
  banknew = int(bank) + int(amount)
  if banknew > user['Bank-Space']:
    return f"You do not have enough bank space to deposit ₹{str(amount)}!"
  moneynew = int(money) - int(amount)
  del user['Money']
  user['Money'] = moneynew
  del user['Bank'] 
  user['Bank'] = banknew
  delete = {"Username": username}
  profilescol.delete_one(delete)
  profilescol.insert_many([user])
  return int(amount)

def settrade(type, username, giveamount, giveitem, recieveamount, recieveitem):
  if type == True:
    print("global trade")
    # document = [{
    #   "Username": username,

    # }]
  else:
    print(f"trade to {type}")