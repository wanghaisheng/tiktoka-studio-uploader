from ytb_up.youtube import *
from datetime import datetime,date,timedelta
import asyncio

profilepath = r'D:\Download\audio-visual\make-text-video\reddit-to-video\assets\profile\fastlane'
CHANNEL_COOKIES = r'D:\Download\audio-visual\make-text-video\reddit-to-video\assets\cookies\aww.json'
CHANNEL_COOKIES = r'D:\Download\audio-visual\saas\tiktoka\ytb-up\cookies\fastlane.json'

videopath = r'D:\Download\audio-visual\saas\tiktoka\ytb-up\tests\1.mp4'
tags = ['ba,baaa,bababa']
publish_date = ''
# if you use some kinda of proxy to access youtube, 
proxy_option = "socks5://127.0.0.1:1080"

# for cookie issue,
title = 'bababala'
title=title[:95]
username = "edwin.uestc@gmail.com"
password = "U437P8Is9prmNquVerHJ9%R00b"
description = '========================'
driverpath = r'D:\Download\audio-visual\make-reddit-video\autovideo\assets\driver\geckodriver-v0.30.0-win64\geckodriver.exe'
thumbnail = r'D:\Download\audio-visual\make-reddit-video\reddit-to-video\assets\ace\ace-attorney_feature.jpg'
upload = YoutubeUpload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    root_profile_directory='',
    proxy_option=proxy_option,
    watcheveryuploadstep=True,
    # if you want to silent background running, set watcheveryuploadstep false
    CHANNEL_COOKIES=CHANNEL_COOKIES,
    username=username,
    password=password,
    closewhen100percentupload=True,
    recordvideo=True
    # for test purpose we need to check the video step by step ,
)
today = date.today()


def instantpublish():

    asyncio.run(upload.upload(
        videopath=videopath,
        title='instant publish-test-005',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        publishpolicy=1
    ))

def saveasprivatedraft():
    asyncio.run(upload.upload(
        videopath=videopath,
        title='private draft-test-004',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        publishpolicy=0
    ))

def scheduletopublish_tomorrow():
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish="10:15"
    #if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=1)
    asyncio.run(upload.upload(
        videopath=videopath,
        title='tomorrow-test-001',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        publishpolicy=2,
        date_to_publish=date_to_publish,
        hour_to_publish=hour_to_publish
    ))



def scheduletopublish_every7days():
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish="10:15"
    #if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=7)
    # hour_to_publish=datetime.strptime(hour_to_publish, "%H:%M")

    # print('after convert',hour_to_publish.strftime("%I:%M %p").strip("0"))

    asyncio.run(upload.upload(
        videopath=videopath,
        title='7days later-test-003',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        publishpolicy=2,
        date_to_publish=date_to_publish,
        hour_to_publish=hour_to_publish
    ))



def scheduletopublish_at_specific_date():
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish="10:15"
    #if you want tomorrow ,just change 7 to 1
    publish_date += timedelta(days=3)
    # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
    asyncio.run(upload.upload(
        videopath=videopath,
        title='four days later-test-002',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        publishpolicy=2,
        date_to_publish=date_to_publish,
        hour_to_publish=hour_to_publish

    ))
        # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow

        #  if release_offset and not release_offset == "0-1":
        #             print('mode a sta',release_offset)
        #             if not int(release_offset.split('-')[0]) == 0:
        #                 offset = timedelta(months=int(release_offset.split(
        #                     '-')[0]), days=int(release_offset.split('-')[-1]))
        #             else:
        #                 offset = timedelta(days=1)
        #             if publish_date is None:
        #                 publish_date =datetime(
        #                     date.today().year,  date.today().month,  date.today().day, 10, 15)
        #             else:
        #                 publish_date += offset
                

# scheduletopublish_tomorrow()
# scheduletopublish_at_specific_date()
scheduletopublish_every7days()
saveasprivatedraft()
instantpublish()