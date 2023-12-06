from upgenius.tiktok.sessionId.uploader import upload2TiktokSessionId
from upgenius.utils.tools import get_duration_timestamp
import pandas  as pd
import os
import json

def more():

    # add the following for each video
    videojson='examples/tiktok-videos.json'
    if videojson and os.path.exists(videojson):
        videos=json.load(open(videojson, 'r', encoding='utf-8')) ['videos']
        print(f'start to load videos in json file, found {len(videos)} videos there')

        for item in videos:
            print(item)
            print(f"start to process {item['path']}")
            url_server='www'

            session_id = item["session_id"]
            title = item["title"]
            path = item["path"]
            tags = item["tags"]
            users = item["users"]
            print(f'type {type(tags)}')
            print(f'type {type(users)}')

            year_target = item["year_target"]
            month_target = item["month_target"]
            day_target = item["day_target"]
            hour_target = item["hour_target"]

            minute_target = item["minute_target"]
            second_target = item["second_target"]

            schedule_time = get_duration_timestamp(year_target, month_target, day_target, hour_target, minute_target, second_target)


            print(f'start to upload video:{path} to tiktok {url_server}')

            isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)
            if isupload==False:

                url_server='us'
                print(f'another try to start to upload video:{path} to tiktok {url_server}')

                isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)
    else:
        print('videos.json file not found')
if __name__ == '__main__':
    more()