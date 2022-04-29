import instaloader
import datetime
from pathlib import Path
import lzma
import os
import json
import shutil
from random import shuffle


class IGBot:
	def __init__(self, username, password, ig_account_list, days_back=6, max_video_time=840, min_video_time=420, max_clip_size=60, min_clip_size=5):
		"""
		This class will scrape videos for every user in ig_account_list that has posted in the last days_back days.
		:param username: Your instagram username.
		:param password: Your instagram password.
		:param days_back: How many days back the IG Bot will download content from.
		The below parameters measure in seconds:
		:param max_video_time: Max length of the video
		:param min_video_time: Min length of the video
		:param max_clip_size: Max length of a clip
		:param min_clip_size: Min length of a clip
		"""
		self.ig_account_list = ig_account_list

		self.max_video_time = max_video_time
		self.min_video_time = min_video_time
		self.max_clip_size = max_clip_size
		self.min_clip_size = min_clip_size
		self.username = username
		self.password = password
		self.days_back = days_back

		self.ig_bot = instaloader.Instaloader()
		self.ig_bot.login(self.username, self.password)

	def get_content(self):
		"""
		Gets the content using the information from the __init__ function.
		:return Boolean: True if there is enough content to make a video. False is there is not.
		"""
		shuffle(self.ig_account_list)  # randomizing the order of the list for more of a different choice in content
		current_day_time_obj = datetime.datetime.today()
		previous_days_time_obj = current_day_time_obj - datetime.timedelta(days=self.days_back)

		total_seconds = 0

		for account in self.ig_account_list:
			acc = instaloader.Profile.from_username(self.ig_bot.context, account)

			print(f"Scraping -> Username: {acc.username} | Followers: {acc.followers} | Posts: {acc.mediacount}")
			posts = acc.get_posts()
			post_count = 0
			for post in posts:
				is_video = post.get_is_videos()
				if len(is_video) == 1:
					if is_video[0]:
						if previous_days_time_obj < post.date_utc < current_day_time_obj:
							if self.min_clip_size <= post.video_duration <= self.max_clip_size:
								download_path = Path(f"content/{acc.username}/{post_count}")
								self.ig_bot.download_post(post, target=download_path)

								xz_filename = [file for file in os.listdir(download_path) if file.endswith(".xz")][0]
								xz_file_path = Path(f"{download_path}/{xz_filename}")
								xz_file_contents = lzma.open(filename=xz_file_path, mode="r")
								json_data = json.loads([data for data in xz_file_contents][0].decode())
								xz_file_contents.close()
								if json_data['node']['has_audio']:
									total_seconds += post.video_duration  # only adding time when the video is kept
									post_count += 1
								else:
									shutil.rmtree(download_path)
						else:
							break
				if total_seconds >= self.max_video_time:  # checking this condition twice to get out of the double loop
					break
			print(f"Downloaded {post_count} videos from {acc.username}")
			print("\n")

			if total_seconds >= self.max_video_time:
				print(
					f"IG Bot has gathered {round(self.max_video_time / 60, 2)} minutes of content. Skipping all the other accounts.")
				break

		print("User list has ended. Program has completed executing.")

		print(f"Total video time: {total_seconds} seconds")

		if total_seconds >= self.min_video_time:
			return True
		else:
			return False
