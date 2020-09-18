import gspread
import datetime
import json

# sheetsData.json = {
#   "type": "",
#   "project_id": "",
#   "private_key_id": "",
#   "private_key": "",
#   "client_email": "",
#   "client_id": "",
#   "auth_uri": "",
#   "token_uri": "",
#   "auth_provider_x509_cert_url": "",
#   "client_x509_cert_url": ""
# }

class Google():
	def __init__(self):
		self.gc = gspread.service_account(filename= 'sheetsData.json')
		self.sheetFollowing = None
		self.sheetFollowers = None
		self.sheetDict = None
		self.toFollowSheet = None
		self.date = datetime.date.today().isoformat()
		self.unfollow = {}
		# self.d = {}
		with open('curiawesityFollowing.json') as f:
			self.d = json.load(f)

	def initSheets(self):
		self.sheetFollowing = self.gc.open('crawler').worksheet(f"curiawesityFollowing")
		self.sheetFollowers = self.gc.open('crawler').worksheet(f"curiawesityFollowers")

	# OLD USE IF FIRST TIME RUNNING (GRABS DATA FROM GOOGLE FOR ALL PAST)
	def getFollowingFollowersFromGoogle(self):
		self.initSheets()
		# gets list of rows from google
		v = self.sheetFollowing.get_all_values()
		d = {}
		for date,href,fol in v:
			if href not in d:
				#working on this!!!!!!!!!!!!!!!!!!!!!
				d[href] = {"following":False,"date_i_followed":date,"date_they_followed":"","date_i_unfollowed":"","likedPhotos":[]}
		# unfollow list and add those who followed back
		v = self.sheetFollowers.get_all_values()
		unfollow = []
		for date,href,fol in v:
			if href in d:
				if d[href]["date_they_followed"] == "":
					d[href]["date_they_followed"] = date
		# test this can be wrong because I have friends who I do not follow.
		# INSTEAD: if "date_they_followed" == "" and "date_i_unfollowed" == "" and today is far enouph from that day, unfollow and set "date_i_unfollowed"
		# self.unfollow = [x for x in d if d[x]["date_they_followed"] == ""]
		self.d = d
		# Save file
		with open('curiawesityFollowing.json', 'w') as outfile:
			json.dump(d, outfile)

	# New needs testing
	def saveMyFollowToGoogle(self, followers_save, followersTags_save,following_save, followingTags_save):
		self.initSheets()
		following = []
		for i, follower in enumerate(following_save):
			following.append([self.date,follower,followingTags_save[i]])
		self.sheetFollowing.append_rows(following)
		followers = []
		for i, follower in enumerate(followers_save):
			followers.append([self.date,follower,followersTags_save[i]])
		self.sheetFollowers.append_rows(followers)
		# Todo:  Check if sheet exists, if no, create, then do this(append)
		# sheet = self.gc.open('crawler').worksheet(f"{user}Following")
		# sheet.append_rows(followers)
		# sheet = self.gc.open('crawler').worksheet(f"{user}Followers")
		# sheet.append_rows(followers)

	def saveDictToGoogle(self, gDict):
		# sheetDict.clear()
		with open('curiawesityFollowing.json') as f:
			self.d = json.load(f)
		d = []
		# d.append()
		i = 0
		for key, value in gDict.d.items():
			if i == 0:
				l = ["href"]
				ll = list(value.keys())
				l.extend(ll + [self.date])
			else:
				l = [key]
				ll = list(value.values())
				l.extend(ll[:3] + [str(ll[3])] + ll[4:])
			d.append(l)
			i+=1
		self.sheetDict = self.gc.open('crawler').worksheet(f"dict")
		self.sheetDict.update('A1', d)
	
	def toFollowGet(self):
		self.toFollowSheet = self.gc.open('crawler').worksheet(f"kurzgesagtFollowing")
		return self.toFollowSheet.col_values(1)