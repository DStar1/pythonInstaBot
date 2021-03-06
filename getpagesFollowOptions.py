from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
import time
import sys
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
		self.hrefs = []
		self.followTags = []
		self.user = user
	def get_num_flw(self, flag):
			if flag == "followers":
					# Followers
					flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{self.user}/followers/\')]")))
					# flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
					sflw = b(flw.get_attribute('innerHTML'), 'html.parser')
					followers = sflw.findAll('span', {'class':'g47SY'})
					f = followers[0].getText().replace(',', '')
			elif flag == "following":
					# Following
					flw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{self.user}/following/\')]")))
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
		time.sleep(2)
		followersOrFollowing = "followers"
		numFollow = self.get_num_flw(followersOrFollowing)
		# Followers
		flw_btn = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, \'/{self.user}/followers/\')]")))
		# flw_btn = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span')))
		# Following
		# flw_btn = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, \'/curiawesity/following/\')]")))
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
				time.sleep(1)
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
					self.hrefs.append(hlink)
					self.followTags.append(followTag)
			except:
				pass
		return self.hrefs, self.followTags

	def get_following(self):
		time.sleep(2)
		followersOrFollowing = "following"
		numFollow = self.get_num_flw(followersOrFollowing)
		# if followersOrFollowing == "followers":
    # 		# Followers
    # 		flw_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span')))
		# elif followersOrFollowing == "following":
    # 		# Following
		#     flw_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, \'/curiawesity/following/\')]")))
		
		# Followers
		#flw_btn = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a > span')))
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
				time.sleep(1)
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
					self.hrefs.append(hlink)
					self.followTags.append(followTag)
			except:
				pass
		return self.hrefs, self.followTags		

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
		# Harrison corrected elem location and added a check to make sure we dont unlike a photo
		like_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > div.ltEKP > article > div > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > div > span > svg')))
		if (like_btn.get_attribute("aria-label") == "Like"):
			like_btn.click()
			return href

	# Newly added by me
	def follow_page(self):
		try:
			# Following already
			follow = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span')))
			f_text = follow.get_attribute("aria-label")
		except:
			follow = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button')))
			f_text = follow.text
		if f_text.lower() == 'follow' or f_text.lower() == 'follow back':
			follow.click()
		elif f_text.lower() == 'following':
			print('already following')
		time.sleep(1)

	def unfollow_page(self):
		unfollow = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span')))
		unfollow.click()
		unfollow = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_')))
		unfollow.click()
		time.sleep(1)

