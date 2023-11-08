from tsup.tiktok.sessionId.uploader import upload2TiktokSessionId
from tsup.utils.tools import get_duration_timestamp
import pandas  as pd
import os
import json

def more():

    # add the following for each video
    videometa='examples/tiktok-videos.xlsx'
    if videometa and os.path.exists(videometa):
        my_dic = pd.read_excel(videometa, engine="openpyxl", index_col=None)

        for name in my_dic.iterrows():
            print(name)
            
            item = name[1].to_dict()        
            print(item)

            # print(f'start to load videos in json file, found {len(videos)} videos there')

        # for item in videos:
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
            try:
                isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)
                if isupload==False:

                    url_server='us'
                    print(f'another try to start to upload video:{path} to tiktok {url_server}')

                    isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)
            except Exception as e:
                print(f'you may double check sessionid is ok :\n {e}')
    else:
        print('videos.json file not found')    
if __name__ == '__main__':
    more()