import os
import csv
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

# https://www.youtube.com/watch?v=Pr0tC-6hh44 - Learn how to use the YouTube API and how to set up your account.


class VideoPublisher:
	def __init__(self,
				 CLIENT_SECRET_FILE="client_secret.json",
				 API_NAME="youtube",
				 API_VERSION="v3",
				 SCOPES=['https://www.googleapis.com/auth/youtube.upload'],
				 video_dir="results",
				 video_filename="video.mp4",
				 video_title_format="TRY NOT TO LAUGH V{video_id}"):

		self.video_dir = video_dir
		self.video_filename = video_filename
		self.video_title_format = video_title_format

		self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
		self.API_NAME = API_NAME
		self.API_VERSION = API_VERSION
		self.SCOPES = SCOPES
		self.service = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

	def get_next_title(self):
		file_exists = os.path.exists("custom_content/video_data.csv")
		if file_exists:
			data = []
			with open("custom_content/video_data.csv", "r", newline="") as csv_file:
				csv_reader = csv.reader(csv_file)
				for row in csv_reader:
					data.append(row)
			last_row = data[-1]

			new_id = str(int(last_row[0]) + 1)
			new_title = last_row[1].split("V")[0] + 'V' + str(int(last_row[1].split("V")[-1]) + 1)
			new_publish_date = str(datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S"))
			new_row = [new_id, new_title, new_publish_date]

			with open("custom_content/video_data.csv", 'a', newline="") as csv_file:
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow(new_row)
			return new_title
		else:
			with open("custom_content/video_data.csv", 'w', newline="") as csv_file:
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow(['Video ID', 'Title', 'Date Published'])
				new_title = f'{self.video_title_format.replace("{video_id}", "1")}'
				csv_writer.writerow(['0', new_title, f'{datetime.datetime.now().strftime("%m/%d/%Y | %H:%M:%S")}'])

			return new_title

	def upload_video(self, title, description, tags, categoryId=23, privacyStatus="public", forKids=False, notify_subscribers=True):

		request_body = {
			'snippet': {
				'categoryId': categoryId,
				'title': title,
				'description': description,
				'tags': tags
			},
			'status': {
				'privacyStatus': privacyStatus,
				'selfDeclaredMadeForKids': forKids,
			},
			'notifySubscribers': notify_subscribers
		}

		media_file = MediaFileUpload(f"{self.video_dir}/{self.video_filename}")

		response_upload = self.service.videos().insert(
			part="snippet,status",
			body=request_body,
			media_body=media_file
		).execute()

		print("--- Video Uploaded Successfully ---")
