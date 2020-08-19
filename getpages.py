from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time
import sys
import datetime
from dateutil.parser import parse

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

class Getpages:
	def __init__(self, driver, user):
		self.driver = driver
		self.driver.get(f'https://www.instagram.com/{user}')
		self.following = []
		self.followingTags = []
		self.followers = []
		self.followersTags = []
		self.user = user
		self.date = datetime.date.today().isoformat()
	def get_num_flw(self, flag, user):
			if flag == "followers":
					# Followers
					flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{user}/followers/\')]")))
					# flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
					sflw = b(flw.get_attribute('innerHTML'), 'html.parser')
					followers = sflw.findAll('span', {'class':'g47SY'})
					f = followers[0].getText().replace(',', '')
			elif flag == "following":
					# Following
					flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{user}/following/\')]")))
					sflw = b(flw.get_attribute('innerHTML'), 'html.parser')
					followers = sflw.findAll('span', {'class':'g47SY'})
					f = followers[0].getText().replace(',', '')
			if 'k' in f:
					f = float(f[:-1]) * 10**3
					return f
			elif 'm' in f:
					f = float(f[:-1]) * 10**6
					return f
			else:
					return float(f)

	def get_followers(self):
		self.driver.get(f'https://www.instagram.com/{self.user}')
		time.sleep(2)
		followersOrFollowing = "followers"
		numFollow = self.get_num_flw(followersOrFollowing, self.user)
		# Followers
		flw_btn = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{self.user}/followers/\')]")))
		flw_btn.click()
		time.sleep(3)
		self.popup = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]')))
		print("MADE IT")
		for h in range(11):
			time.sleep(1)
			print('scrolling')
			print(h)
			print('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)))
			self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)), self.popup)
			if h == 5:
				break
    	# num follow
		currentFollow = 0
		#for i in range(3):#70):#numFollow:
		print("GETTING FOLLOWERS")
		while currentFollow < numFollow:
				time.sleep(2)
				self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', self.popup)
				# loads 36 at a time
				currentFollow += 10
				update_progress(currentFollow/numFollow)
				#print(currentFollow/numFollow+"%")
		self.popup = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]')))
		b_popup = b(self.popup.get_attribute('innerHTML'), 'html.parser')
		for p in b_popup.findAll('li', {'class': 'wo9IH'}):
			try:
				hlink = p.find_all('a')[0]['href']
				followTag = p.find_all('button')[0].text
				# followTags = [f for f in followTag]
				print(hlink, ", ", followTag)
				if 'div' in hlink:
					print('div found not adding to list')
				else:
					self.followers.append(hlink)
					self.followersTags.append(followTag)
			except:
				pass
		return self.followers, self.followersTags

	def get_following(self):
		self.driver.get(f'https://www.instagram.com/{self.user}')
		time.sleep(2)
		followersOrFollowing = "following"
		numFollow = self.get_num_flw(followersOrFollowing, self.user)
		# Following
		flw_btn = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{self.user}/following/\')]")))
		flw_btn.click()
		time.sleep(3)
		self.popup = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]')))
		print("MADE IT")
		for h in range(11):
			time.sleep(1)
			print('scrolling')
			print(h)
			print('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)))
			self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)), self.popup)
			if h == 5:
				break
    	# num follow
		currentFollow = 0
		#for i in range(3):#70):#numFollow:
		print("GETTING FOLLOWERS")
		while currentFollow < numFollow:
				time.sleep(2)
				self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', self.popup)
				# loads 36 at a time
				currentFollow += 10
				update_progress(currentFollow/numFollow)
				#print(currentFollow/numFollow+"%")
		self.popup = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]')))
		b_popup = b(self.popup.get_attribute('innerHTML'), 'html.parser')
		for p in b_popup.findAll('li', {'class': 'wo9IH'}):
			try:
				hlink = p.find_all('a')[0]['href']
				followTag = p.find_all('button')[0].text
				# followTags = [f for f in followTag]
				print(hlink, ", ", followTag)
				if 'div' in hlink:
					print('div found not adding to list')
				else:
					self.following.append(hlink)
					self.followingTags.append(followTag)
			except:
				pass
		return self.following, self.followingTags		

	def is_public(self):
		try:
			astate = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'rkEop')))
			if astate.text == 'This Account is Private':
				return False
			else:
				return True
		except:
			return True

	def like_post(self):
		post = self.driver.find_element_by_css_selector('#react-root > section > main > div > div._2z6nI > article > div > div > div:nth-child(1) > div:nth-child(1)')
		html = post.get_attribute('innerHTML')
		h = b(html, 'html.parser')
		href = h.a['href']
		self.driver.get('https://www.instagram.com' + href)
		# Get date
		date_obj = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[2]/a/time')))#//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[2]/a/time
		date = date_obj.get_attribute("datetime")
		# pic_date = datetime.strptime(date[:10], '%Y-%m-%d')
		pic_date = parse(date)
		now = datetime.datetime.now(pic_date.tzinfo)
		# print(f"{pic_date}\n{now}\n{now - datetime.timedelta(3)}\n\n")
		daysPadding = 10
		if pic_date >= now - datetime.timedelta(daysPadding):
			# Harrison corrected elem location and added a check to make sure we dont unlike a photo
			like_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > div > span > svg')))#'#react-root > section > main > div > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > div > span > svg > path////*[@id="react-root"]/section/main/div/div/article/div[3]/section[1]/span[1]/button/div/span/svg/path
			if (like_btn.get_attribute("aria-label") == "Like"):
				like_btn.click()
				print("Liked succefully")
				return href
			else:
				print("Already liked?")
		else:
			print(f"Pic older than {daysPadding} days")

	# Newly added by me
	def follow_page(self, href):
		try:
			# Public
			follow = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button')))#'//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span')))
			# f_text = follow.get_attribute("aria-label")	
			f_text = follow.text
		except:
			# Private
			follow = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/button')))#//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button')))
			f_text = follow.text
		if f_text.lower() == 'follow' or f_text.lower() == 'follow back':
			follow.click()
			print('followed')
			time.sleep(1)
			return 1
		elif f_text.lower() == 'following':
			print('already following')
		return 0

	def unfollow_page(self):
		try:
			unfollow = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span')))
		except:
			unfollow = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/button/div/span')))
		time.sleep(1)
		if unfollow.get_attribute("aria-label") == "Following":
			unfollow.click()																		   
			unfollow = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_')))
			if unfollow.text == "Unfollow":
				unfollow.click()
				time.sleep(1)
				return 1
		return 0
