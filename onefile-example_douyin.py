# from ytb_up import *
from ytb_up.douyin import DouyinUpload
from datetime import datetime,date,timedelta
import asyncio
import json
profilepath = ''
CHANNEL_COOKIES='assets/douyin-cookie.json'
videopath = 'assets/hello.mp4'
tags = ['ba,baaa,bababa']
publish_date = ''
# if you use some kinda of proxy to access youtube, 
proxy_option = "socks5://127.0.0.1:1080"
proxy_option=''
# for cookie issue,
title = 'bababala'
title=title[:95]
username = "antivte"
password = ""
description = '========================'
thumbnail = './9-16.jpeg'
thumbnail = './hello.png'

upload = DouyinUpload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    root_profile_directory='',
    proxy_option=proxy_option,
    watcheveryuploadstep=True,
    # if you want to silent background running, set watcheveryuploadstep false
    CHANNEL_COOKIES=CHANNEL_COOKIES,
    username=username,
    password=password,
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
        closewhen100percentupload=True,
        location='深圳',
        miniprogram='',
        heji='heji1',
        hottopic='老公',
        up2toutiao=False,
        allow2save=True,
        allow2see='公开',
        publishpolicy='立即发布'
    ))

def saveasprivatedraft():
    asyncio.run(upload.upload(
        videopath=videopath,
        title='private draft-test-004',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        closewhen100percentupload=True,
        publishpolicy=0
    ))

def scheduletopublish_tomorrow():
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    asyncio.run(upload.upload(
        videopath=videopath,
        title='instant publish-test-005',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        closewhen100percentupload=True,
        location='深圳市',
        miniprogram='',
        heji='heji1',
        hottopic='老公',
        up2toutiao=False,
        allow2save=True,
        allow2see='公开',
        publishpolicy='定时发布',
        publish_date=publish_date

    ))



def scheduletopublish_7dayslater():
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    publish_date += timedelta(days=7)
    asyncio.run(upload.upload(
        videopath=videopath,
        title='7days later-test-003',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        release_offset='0-1',
        closewhen100percentupload=True,
        publishpolicy=2,
        publish_date=publish_date
    ))



def scheduletopublish_specific_date():
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want tomorrow ,just change 7 to 1
    publish_date += timedelta(days=3)
    # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
    asyncio.run(upload.upload(
        videopath=videopath,
        title='four days later-test-002',
        description=description,
        thumbnail=thumbnail,
        tags=tags,
        closewhen100percentupload=True,
        publishpolicy=2,
        publish_date=publish_date

    ))


# scheduletopublish_specific_date()
# scheduletopublish_7dayslater()
# saveasprivatedraft()
# instantpublish()
scheduletopublish_tomorrow()
