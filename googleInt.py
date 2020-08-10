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
		self.sheetFollowing = self.gc.open('crawler').worksheet(f"curiawesityFollowing")
		self.sheetFollowers = self.gc.open('crawler').worksheet(f"curiawesityFollowers")
		self.date = datetime.date.today().isoformat()
		self.unfollow = {}
		# self.d = {}
		with open('curiawesityFollowing.json') as f:
			self.d = json.load(f)

	# OLD USE IF FIRST TIME RUNNING (GRABS DATA FROM GOOGLE FOR ALL PAST)
	def getFollowingFollowersFromGoogle(self):
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