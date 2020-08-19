from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time
import login
import getpages
import csv
import pandas as pd
import datetime
import googleInt
import updateDict
import random
from dateutil.parser import parse
from bots import followersFollowing, unfollow_bot, like_bot, checkRefollow, follow_bot, followUnfollowLikeHour
import json
# ############################ IMPORTANT!!!!!!!! ##########
# config.json = {
#     "username": "USERNAME",
#     "password": "PASSWORD",
#     "user": "USER(CAN BE SAME AS USERNAME, UNLESS PULLING DATA FROM ANOTHER USER)"
# }
try:
	with open("config.json") as f:
		c = json.load(f)
except:
	print("Add config file!")

username = c["username"]
password = c["password"]
user = c["user"]
driver = 0
refs = []
max_likes = 20#350
max_follows = 20#50
def set_driver():
	# #With browser
	driver = webdriver.Chrome('/Users/harrison/Downloads/chromedriver')
	# #Without browser
	# op = webdriver.ChromeOptions()
	# op.add_argument('headless')
	# driver = webdriver.Chrome(options=op)
	################ No browser Google Colab ###################
	# options = webdriver.ChromeOptions()
	# options.add_argument('--headless')
	# options.add_argument('--no-sandbox')
	# options.add_argument('--disable-dev-shm-usage')
	# # open it, go to a website, and get results
	# wd = webdriver.Chrome('chromedriver',options=options)
  	################# No browser Mac ###################
	# options = Options()
	# options.headless = True
	# driver = webdriver.Chrome('chromedriver', chrome_options=options)
	return driver

# if __name__ == '__main__':
# global driver
print('running script..')
driver = set_driver()
# input() # Get VPN if needed
l = login.Login(driver, username, password)
time.sleep(2)
l.signin()
time.sleep(2)
gp = getpages.Getpages(driver, user)
time.sleep(2)
followers, followersTag, following, followingTag = followersFollowing(gp, user)
print("GOT FOLLOWERS AND FOLLOWING")
# Find a way to check if, out of the new shortened list of following, a person has been unfollowed, and label it todays date
# Go through list, and label all who are followed still, then unfollow all others
# d[href]["following"] = True(if I am still following)
############# Update dict
gDict = updateDict.UpdateDict()
gDict.updateFollowingFollowersDict(followers,following)
goog = googleInt.Google()
max_likes = 20#350
max_follows = 20#50
# reference dict with (g.d)
g = None
name = ""
while name != "done":
	name = input("Conitue?\nOPTIONS(like, unfollow, follow, checkRefollow, google, update, done): ")
	if name == "done":
		print("Exiting")
		break
	elif name == "unfollow":
		print(f"Unfollowing {max_follows}")
		unfollow_bot(gDict, gp, max_follows)
	elif name == "like":
		print(f"Liking {max_likes}")
		like_bot(gDict, gp, max_likes)
	elif name == "follow":
		print("No follow function")
		follow_bot(goog, gDict, gp)#, max_follows = 40)
	elif name == "update":
		followers, followersTag, following, followingTag = followersFollowing(gp, user)
		gDict.updateFollowingFollowersDict(followers,following)
		try:
			goog.saveDictToGoogle(gDict)
		except:
			print("Unable to save to dict to google sheets...")
	elif name == "checkRefollow":
		checkRefollow(gDict)
	elif name == "google":
		# ############ Saves my followers and following to google sheets for backup ########
		if not g:
			g = googleInt.Google()
		g.saveMyFollowToGoogle(followers, followersTag,following, followingTag)
		# print("SAVED FOLLOWERS AND FOLLOWING TO GOOGLE")

driver.quit()



# import xmltodict
# import pprint
# import json

# with open('person.xml') as fd:
#     doc = xmltodict.parse(fd.read())

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json.dumps(doc))

# import sys, select
# def timeout_input(prompt, timeout=3, default=""):
# 	print(prompt, end=': ', flush=True)
# 	inputs, outputs, errors = select.select([sys.stdin], [], [], timeout)
# 	print()
# 	return (0, sys.stdin.readline().strip()) if inputs else (-1, default)

# def followUnfollowLikeHour(gDict, gp, max_follows, max_likes):
# 	i = 1
# 	while True:
# 		print(f"Ran {i} times:\n")
# 		i+=1
# 		unfollow_bot(gDict, gp, max_follows)
# 		follow_bot(goog, gDict, gp)
# 		like_bot(gDict, gp, max_likes, max_follows)
# 		if timeout_input("MAIN LOOP: Press enter to stop: ",3600) != (-1, ''):
# 			break

print("done")
