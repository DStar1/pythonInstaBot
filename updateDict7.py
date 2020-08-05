import datetime
import json

class UpdateDict():
	def __init__(self):
		self.date = datetime.date.today().isoformat()
		# self.d = {}
		with open('curiawesityFollowing.json') as f:
			self.d = json.load(f)

	# Doesn't belong in Google Class
	def updateFollowingFollowersDict(self, followers, following):
		# gets list of rows
		# v = self.sheetFollowing.get_all_values()
		# Clearn I still following
		for href in self.d.keys():
			self.d[href]["i_still_following"] = False
		# Add new following and update i still following
		for href in following:
			if href not in self.d:
				#working on this!!!!!!!!!!!!!!!!!!!!!
				self.d[href] = {"date_i_followed":self.date,"date_they_followed":"","date_unfollow":"","likedPhotos":[],"they_still_following":False, "date_they_unfollowed":"","i_still_following":True}
			else:
				self.d[href]["i_still_following"] = True
				# If I refollow someone
				self.d[href]["date_unfollow"] = ""
		# Updates all in dict to not following, so only people currently following show (below)
		for href in self.d.keys():
			self.d[href]["they_still_following"] = False
		# unfollow list and add those who followed back
		for href in followers:
			if href in self.d:
				if self.d[href]["date_they_followed"] == "":
					self.d[href]["date_they_followed"] = self.date
				self.d[href]["they_still_following"] = True
		for href in self.d.keys():
			# Keep track if they unfollow me, but I didn't unfollow them
			if self.d[href]["date_they_followed"] != "" and self.d[href]["they_still_following"] == False and self.d[href]["date_they_unfollowed"] == "":
				self.d[href]["date_they_unfollowed"] = self.date
			if self.d[href]["date_i_followed"] != "" and self.d[href]["i_still_following"] == False and self.d[href]["date_unfollow"] == "":
				self.d[href]["date_unfollow"] = self.date
		# test this can be wrong because I have friends who I do not follow.
		# INSTEAD: if "date_they_followed" == "" and "date_i_unfollowed" == "" and today is far enouph from that day, unfollow and set "date_i_unfollowed"
		# self.unfollow = [x for x in d if d[x]["date_they_followed"] == ""]
		self.saveJson()

	def unfollow(self, href):
		self.d[href]["date_unfollow"] = self.date
		self.d[href]["i_still_following"] = False
		self.saveJson()

	# def follow(self, href):
	# 	self.d[href]["date_i_followed"] = self.date
	# 	["i_still_following"] = True
	# 	self.saveJson()

	def saveJson(self):	
		# Save file
		with open('curiawesityFollowing.json', 'w') as outfile:
			json.dump(self.d, outfile)
		
		# No need. Dict preserves oder from oldest I followed to newest.
		# self.unfollow = sorted(self.d.items(), key=lambda x:x["date_i_followed"], reverse=False)