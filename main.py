from igbot import IGBot
from video_compiler import VideoCompiler
from video_publisher import VideoPublisher
import os
import shutil
from random import shuffle

# add more IG users to this list if you want
ig_account_list = ['meme_dealer', 'hits_the_blunt', 'gameland', 'petovers', 'radical_homo', 'pampam.mp4',
                   'submityourvideos', 'lmao', 'memes.hub.indian', 'hollow_pineapple', 'bruh.bruhhhhhhhhhhh']


class SchedulerBot:
    def __init__(self):
        # Posting on Monday 8pm will get content from Monday, Sunday, Saturday. Posting on Friday 8pm will get content
        # from Friday, Thursday, Wednesday. MAX = ~10:00, MIN = 7:30
        self.ig_bot = IGBot("your_ig_bot_username", "and_your_password", ig_account_list, days_back=3,
                            max_video_time=600, min_video_time=450, max_clip_size=60, min_clip_size=5)
        self.video_compiler = VideoCompiler("content", "results", "video.mp4")
        self.video_publisher = VideoPublisher(CLIENT_SECRET_FILE="client_secret.json",
                                              API_NAME="youtube",
                                              API_VERSION="v3",
                                              SCOPES=['https://www.googleapis.com/auth/youtube.upload'],
                                              video_dir="results",
                                              video_filename="video.mp4",
                                              video_title_format="TRY NOT TO LAUGH COMPILATION V{video_id}"
                                              )

    def start_making_a_video(self):
        enough_content = self.ig_bot.get_content()
        if enough_content:
            self.video_compiler.compile_video()
            description = f"""This is the description.
"""

            tags = ["best memes compilation", "memes compilation", "meme compilation", "dank memes compilation",
                    "dank compilation", "memes", "dank memes vine compilation", "tiktok compilation", "best memes",
                    "funny memes", "fresh memes", "dank meme compilation", "dank memes", "minecraft memes",
                    "tik tok memes", "fails compilation", "best memes compilation v71", "dank memes compilations",
                    "weird videos compilation", "memes 2021", "memes 2022", "memes 2023", "tiktok memes", "clean memes",
                    "best memes compilation v69"]
            shuffle(tags)

            print("Uploading video...")

            self.video_publisher.upload_video(title=self.video_publisher.get_next_title(), description=description,
                                              tags=tags, categoryId=23, privacyStatus="public", forKids=False,
                                              notify_subscribers=True)
            print("--- CLEANING UP ---")
            is_success = self.clean_up()
            print("Removed all old content." if is_success else "Content not removed. ERROR!")
        else:
            print("Not making the video! There is an issue. Please investigate.")

        input("Press Enter To Exit...")

    def clean_up(self):
        if os.path.isdir("content"):
            for d in os.listdir("content/"):
                shutil.rmtree(f"content/{d}")
            os.remove('results/video.mp4')
            return True
        return False


scheduler_bot = SchedulerBot()

if __name__ == "__main__":
    scheduler_bot.start_making_a_video()

# You can use the below code to schedule this program. This will allow you to upload the YouTube bot to a server and
# run it automatically.

# import schedule
# import time

# schedule.every().monday.at("09:00").do(job)  # edit this
# schedule.every().friday.at("09:00").do(job)  # and this line if needed by looking at the 'schedule docs'

# while True:
#     schedule.run_pending()
#     time.sleep(1)  # also extend this if it's too short
