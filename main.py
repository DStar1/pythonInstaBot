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

username = 'curiawesity'
password = ''
# ############################ IMPORTANT!!!!!!!! ##########
user = "curiawesity"
driver = 0
refs = []
max_likes = 350
max_follows = 10#50

def call(user):
	global driver
	print('running script..')
	# #With browser
	driver = webdriver.Chrome('/Users/harrison/Downloads/chromedriver')
	# #Without browser
	# op = webdriver.ChromeOptions()
	# op.add_argument('headless')
	# driver = webdriver.Chrome(options=op)
	# #No browser:
	# Colab
	# options = webdriver.ChromeOptions()
	# options.add_argument('--headless')
	# options.add_argument('--no-sandbox')
	# options.add_argument('--disable-dev-shm-usage')
	# # open it, go to a website, and get results
	# wd = webdriver.Chrome('chromedriver',options=options)

  # Mac
	# options = Options()
	# options.headless = True
	# driver = webdriver.Chrome('chromedriver', chrome_options=options)

	l = login.Login(driver, username, password)
	l.signin()
	gp = getpages.Getpages(driver, user)
	followers, followersTag = gp.get_followers()
	print("DONE GETTING FOLLOWERS")
	dfList = {'followers': followers,'followersTag': followersTag}
	df = pd.DataFrame(dfList, columns=['followers', "followersTag"])
	df.to_csv('followers.csv')
	print("DONE SAVING")
	following, followingTag = gp.get_following()
	print("DONE GETTING FOLLOWING")	
	dfList2 = {'following': following,'followingTag': followingTag}
	df2 = pd.DataFrame(dfList2, columns=['following', "followingTag"])
	df2.to_csv('following.csv')
	print("DONE SAVING")

	return followers, followersTag, following, followingTag

if __name__ == '__main__':
	g = googleInt.Google()
	followers, followersTag,following, followingTag = call(user)
	print("GOT FOLLOWERS AND FOLLOWING")
	# # Saves my followers and following to google sheets for backup
	# g.saveMyFollowToGoogle(followers, followersTag,following, followingTag)
	# print("SAVED FOLLOWERS AND FOLLOWING")

	# Find a way to check if, out of the new shortened list of following, a person has been unfollowed, and label it todays date
	# Go through list, and label all who are followed still, then unfollow all others
	# d[href]["following"] = True(if I am still following)
	gDict = updateDict.UpdateDict()
	gDict.updateFollowingFollowersDict(followers,following)
	# reference dict with (g.d)
	unfollow_bot(gDict, gp)


def unfollow_bot(gDict, gp):
	print(len(refs))
	print('accounts targeted')
	t = time.time()
	#how many pages we likes / followed
	L = 0
	F = 0
	for key, value in gDict.d.items():
		if value["they_still_following"] == False and value["i_still_following"] == True:
			gp.driver.get('https://www.instagram.com' + r)
			if gp.get_num_flw("followers") < 3000:
				print("Unfollowing:", key)
				time.sleep(2)
				print('current follows: ' + str(F))
				if F < max_follows:
					time.sleep(5)
					try:
						gp.unfollow_page()
						print('page unfollowed successfully')
						gDict.unfollow(key)
						F += 1
					except:
						print('could not unfollow')
				else:
					time.sleep(3600)



def run_bot(refs, driver, gp):
	#global href dict of everyone I followed and who follows me back
	# usersDictList = {
	# 	"href": "/test/",
	# 	"info": {"href": "/test/","date_i_followed":"01-01-2020","date_they_followed":None,"date_unfollow":"01-07-2020","liked_photos":["id's"]}
	# }
	# List of people to follow from other channels
	listToFollow = ["/test1/", "/test2/"]
	# load/read json
with open('curiawesityFollowing.json') as f:
	d = json.load(f)

	print(len(refs))
	print('accounts targeted')
	t = time.time()
	#how many pages we likes / followed
	L = 0
	F = 0
	for r in listToFollow:
		driver.get('https://www.instagram.com' + r)
		time.sleep(2)
		if gp.get_num_flw("followers") < 3000:
			if gp.is_public():
				print('public account')
				print('current likes: ' + str(L))
				if L < max_likes:
					try:
						gp.like_post()
						L += 1
						print("POST LIKED")
					except:
						print('could not like..lets follow instead')
						# try:
						# 	gp.follow_page()
						# 	print('page followed successfully')
						# 	F += 1
						# except:
						# 	print('could not follow')
				else:
					time.sleep(3600) # time.sleep(3600 - (time.time() - t)) -> t= time.time()
			else:
				print('account is private')
			print('current follows: ' + str(F))
			if F < max_follows:
				time.sleep(2)
				try:
					gp.follow_page()
					print('page followed successfully')
					F += 1
				except:
					print('could not follow')
				
			else:
				time.sleep(3600)

def run_old__bot(refs, driver, gp):
	print(len(refs))
	print('accounts targeted')
	t = time.time()
	#how many pages we likes / followed
	L = 0
	F = 0
	for r in refs:
		driver.get('https://www.instagram.com' + r)
		time.sleep(2)
		if gp.get_num_flw("followers") < 3000:
			if gp.is_public():
				print('public account')
				print('current likes: ' + str(L))
				if L < max_likes:
					try:
						gp.like_post()
						L += 1
						print("POST LIKED")
					except:
						print('could not like..lets follow instead')
						try:
							gp.follow_page()
							print('page followed successfully')
							F += 1
						except:
							print('could not follow')
				else:
					time.sleep(3600) # time.sleep(3600 - (time.time() - t)) -> t= time.time()
			else:
				print('account is private')
				print('current follows: ' + str(F))
				if F < max_follows:
					time.sleep(2)
					try:
						gp.follow_page()
						print('page followed successfully')
						F += 1
					except:
						print('could not follow')
					
				else:
					time.sleep(3600)
