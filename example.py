from ytb_up import *
from datetime import datetime,date,timedelta
import asyncio

profilepath = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\profile\aww'
CHANNEL_COOKIES = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'

videopath = r'D:\Download\audio-visual\objection_engine\hello.mp4'
tags = ['ba,baaa,bababa']
publish_date = ''
proxy_option = 'sad'
title = 'bababala'
username = "antivte"
password = ""
description = '========================'
driverpath = r'D:\Download\audio-visual\make-reddit-video\autovideo\assets\driver\geckodriver-v0.30.0-win64\geckodriver.exe'
thumbnail = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\ace\ace-attorney_feature.jpg'
upload = Upload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    root_profile_directory='',
    proxy_option=proxy_option,
    headless=True,
    CHANNEL_COOKIES=CHANNEL_COOKIES,
    username=username,
    password=password,
)
today = date.today()
# publish_date=''
# if len(videofiles)<int(setting['dailycount']):
#     # publish_date =today+timedelta(days=1)
#     publish_date = datetime(today.year, today.month, today.day+1, 20, 15)

# else:
#     if i <int(setting['dailycount']):
#         publish_date =datetime(today.year, today.month, today.day+1, 20, 15)

#     else:

#         publish_date = datetime(today.year, today.month+int(int(i)/30), today.day+1+int(int(i)/int(setting['dailycount'])), 20, 15)
publish_date = datetime(today.year, today.month, today.day, 10, 15)
publish_date += timedelta(days=7)
publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
process100=1
asyncio.run(upload.upload(
    videopath,
    title=title[:95],
    description=description,
    thumbnail=thumbnail,
    tags=tags,
    process100=process100,
    publishpolicy=2
))


# $ git push origin  playwright