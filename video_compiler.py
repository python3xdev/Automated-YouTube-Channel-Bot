from moviepy.editor import VideoFileClip, concatenate_videoclips

import os
from pathlib import Path
from random import shuffle


class VideoCompiler:
    def __init__(self, content_dir="content", video_save_dir="results", video_filename="video.mp4"):
        self.content_dir = content_dir
        self.video_save_dir = video_save_dir
        self.video_filename = video_filename
        self.video_size = (1920, 1080)

    def get_video_paths(self):
        ''' The Format:
        {
            'username': {'0': 'video.mp4', '1': 'video.mp4', '2': 'video.mp4'},
            'username2': {'0': 'video.mp4', '1': 'video.mp4', '2': 'video.mp4'}
        }
        '''
        acc_dir = os.listdir(self.content_dir)
        result = {}
        for acc in acc_dir:
            acc_dict = {}
            for numbered_folder in os.listdir(Path(f"{self.content_dir}/{acc}")):
                for file in os.listdir(Path(f"{self.content_dir}/{acc}/{numbered_folder}")):
                    if file.endswith(".mp4"):
                        acc_dict[numbered_folder] = file

            result[acc] = acc_dict

        return result

    def compile_video(self):
        content_dict = self.get_video_paths()

        print(content_dict)
        all_ready_clips = []
        for acc in content_dict:
            print(f"Resizing videos from: {acc}")
            for numbered_folder in content_dict[acc]:
                print("Next Clip...")
                new_clip = VideoFileClip(
                    f"{self.content_dir}/{acc}/{numbered_folder}/{content_dict[acc][numbered_folder]}",
                    target_resolution=(self.video_size[1], None))

                if new_clip.w > 1920:
                    new_clip = new_clip.resize(width=self.video_size[0])
                    # OR
                    # new_clip = new_clip.fx(vfx.resize, width=1920)  # https://zulko.github.io/moviepy/getting_started/effects.html

                all_ready_clips.append(new_clip)

        print("Shuffling the clips...")
        shuffle(all_ready_clips)
        print("Clips shuffled!")

        print("Concatinating Video Clips...")

        whole_video = concatenate_videoclips([VideoFileClip(f"custom_content/yt_intro.mp4", target_resolution=(self.video_size[1], None))] + all_ready_clips + [VideoFileClip(f"custom_content/yt_outro.mp4", target_resolution=(self.video_size[1], None))], method="compose")
        # This "compose" argument will put the clips with smaller size in the center of the biggest clip size.

        print("Video clips concatenated!")

        print("Writing video...")

        whole_video.write_videofile(filename=f"{self.video_save_dir}/{self.video_filename}", remove_temp=True)

        print("Video saved!")

        return True
