from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time
import csv
import pandas as pd
import datetime
import random
from dateutil.parser import parse

def followersFollowing(gp, user):
	followers, followersTag = gp.get_followers()
	if len(followers) < gp.get_num_flw("followers", user) - 2:
		print("DIDN'T LOAD ALL FOLLOWERS")
		exit()
	print("DONE GETTING FOLLOWERS")
	dfList = {'followers': followers,'followersTag': followersTag}
	df = pd.DataFrame(dfList, columns=['followers', "followersTag"])
	df.to_csv('followers.csv')
	print("DONE SAVING")
	following, followingTag = gp.get_following()
	if len(following) < gp.get_num_flw("following", user) - 2:
		print("DIDN'T LOADALL FOLLOWING")
		exit()
	print("DONE GETTING FOLLOWING")	
	dfList2 = {'following': following,'followingTag': followingTag}
	df2 = pd.DataFrame(dfList2, columns=['following', "followingTag"])
	df2.to_csv('following.csv')
	print("DONE SAVING")
	return followers, followersTag, following, followingTag

import sys, select
def timeout_input(prompt, timeout=3, default=""):
	print(prompt, end=': ', flush=True)
	inputs, outputs, errors = select.select([sys.stdin], [], [], timeout)
	print()
	return (0, sys.stdin.readline().strip()) if inputs else (-1, default)

def unfollow_bot(gDict, gp, max_follows):
	print('accounts targeted')
	daysPadding = 7
	t = time.time()
	# how many pages we likes/followed
	L = 0
	F = 0
	now = datetime.datetime.now()
	for key, value in gDict.d.items():
		if value["they_still_following"] == False and value["i_still_following"] == True:
			# Todo: Make sure not rescenct follow(past week)
			follow_date = parse(value["date_i_followed"])
			print(f"\n{key}:\nFollow date: {value['date_i_followed']}")
			if now - datetime.timedelta(daysPadding) > follow_date:
				gp.driver.get('https://www.instagram.com' + key)
				# key[1:-1] because "/user/" needs to be "user"
				num_flw = gp.get_num_flw("followers", key[1:-1])
				max_followers = 3000
				if num_flw < max_followers:
					print(f"Num flws(less than {max_followers}): {num_flw}")
					time.sleep(2)
					print(f'current unfollows: {str(F)} of {max_follows}')
					if F < max_follows:
						time.sleep(random.randint(5,10))
						try:
							if gp.unfollow_page():
								print(f'{key}: unfollowed successfully')
								if gDict.unfollow(key):
									print("Updated dict succesfully")
								else:
									print("Updated dict error")
								F += 1
							else:
								print(f'Could not unfollow(problem finding selenium elements)')
						except:
							print(f'{key}: could not unfollow')
					else:
						return
						# time.sleep(3600)
			else:
				print(f"Followed less than {daysPadding} days ago...")

def like_bot(gDict, gp, max_likes):
	print('LIKING')
	t = time.time()
	#how many pages we likes / followed
	L = 0
	F = 0
	# This is a temporary fix. Not neccesary because I will be liking newer photos. not just people who I havent liked their photos
	pics_len = 1
	while L < max_likes:
		# for key, value in gDict.d.items():
		key, value = random.choice(list(gDict.d.items()))
		# timeBefore = time.time()
		if value["i_still_following"] and len(value["likedPhotos"]) < pics_len:
			if timeout_input("Press enter to stop: ") == (-1, ''):
				gp.driver.get('https://www.instagram.com' + key)
				if gp.is_public():
					# key[1:-1] because "/user/" needs to be "user"
					num_flw = gp.get_num_flw("followers", key[1:-1])
					time.sleep(2)
					print('current likes: ' + str(L))
					print(f'{key}: attempting to like')
					time.sleep(random.randint(5,10))
					try:
						photo = gp.like_post()
						if photo:
							print(f'{key}: liked successfully')
							# Not yet implimented
							gDict.like(key,photo)
							L += 1
					except:
						print(f'{key}: could not like')
			else:
				return
		pics_len += 1
	return

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
		if gp.get_num_flw("followers", r) < 3000:
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
		# https://www.instagram.com
		time.sleep(2)
		if gp.get_num_flw("followers", r) < 3000:
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