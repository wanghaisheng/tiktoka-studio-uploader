import argparse
from youtube_uploader_selenium import YouTubeUploader
from typing import Optional

import json
import os


if __name__ == "__main__":
    with open('final_sleep_video.json',encoding='utf8') as json_file:
        videos = json.load(json_file)
        for v in videos:
            v_src = v['path']
            if not os.path.isfile(v_src):
                print(v_src + ' not exist')
                continue
            
            print(v)
            uploader = YouTubeUploader(v)
            was_video_uploaded, video_id = uploader.upload()
            if was_video_uploaded:
                print('rm ' + v_src)
                os.remove(v_src)
            
            break
        

