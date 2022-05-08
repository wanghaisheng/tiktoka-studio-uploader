from ytb_up import *
from datetime import datetime,date,timedelta
import asyncio
import os
##prepare video and thumbnail with the same filename in pair, for example, 
# -1.mp4 
# -1.jpg
# -2.mp4
# -2.png


def check_video_thumb_pair(folder):
    # print('detecting----------',folder)
    videofiles = []

    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            print('detecting----------',r)

            pairedvideothumbs=[]
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    print(filename,'==',ext) 

                    start_index=0
                    if ext in ('.mp4'):
                    # if ext in ('.flv', '.mp4', '.avi'):

                        for image_ext in ('.jpeg', '.png', '.jpg'):
                            videopath = os.path.join(r, entry.name)
                            thumbpath = os.path.join(r, filename+image_ext)

                            if os.path.exists(thumbpath):     
                                video={
                                "thumbpath":thumbpath,
                                "videopath":videopath,
                                "filename":filename

                                }  
                                videofiles.append(video)                 

                                # print('========',videopath)
                                # print('========',thumbpath)

        # for dirs in d:
        #     print(dirs)  
        #     check_video_thumb_pair_basic(dirs)
    return videofiles



profilepath = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\profile\aww'
CHANNEL_COOKIES = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'

videofolder = r'D:\Download\audio-visual\objection_engine'
prefertags = ['ba,baaa,bababa']
publish_date = ''
proxy_option = "socks5://127.0.0.1:1080"
username = "antivte"
password = ""
description = '========================'
#you can set prefered description

driverpath = r'D:\Download\audio-visual\make-reddit-video\autovideo\assets\driver\geckodriver-v0.30.0-win64\geckodriver.exe'
thumbnail = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\ace\ace-attorney_feature.jpg'
upload = Upload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    root_profile_directory='',
    proxy_option=proxy_option,
    watcheveryuploadstep=True,
    CHANNEL_COOKIES=CHANNEL_COOKIES,
    username=username,
    password=password,
)
today = date.today()
publish_date=''
setting={}
setting['dailycount']=20

def scheduletopublish_tomorrow(videopath,thumbpath,filename):
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    # publish_date += timedelta(days=1)
    asyncio.run(upload.upload(
        videopath,
        title=filename[:95],
        description=description,
        thumbnail=thumbpath,
        tags=prefertags,
        release_offset='0-1',
        closewhen100percentupload=True,
        publishpolicy=2,
        publish_date=publish_date
    ))



def scheduletopublish_7dayslater(videopath,thumbpath,filename):
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    publish_date += timedelta(days=7)
    asyncio.run(upload.upload(
        videopath,
        title=filename[:95],
        description=description,
        thumbnail=thumbpath,
        tags=prefertags,
        release_offset='0-1',
        closewhen100percentupload=True,
        publishpolicy=2,
        publish_date=publish_date
    ))



def scheduletopublish_specific_date(videopath,thumbpath,filename):
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want tomorrow ,just change 7 to 1
    publish_date += timedelta(days=3)
    # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
    asyncio.run(upload.upload(
        videopath,
        title=filename[:95],
        description=description,
        thumbnail=thumbpath,
        tags=prefertags,
        closewhen100percentupload=True,
        publishpolicy=2,
        publish_date=publish_date

    ))


videofiles=check_video_thumb_pair(videofolder)
videocount=len(videofiles)

for i in range(videocount):
    if i <int(setting['dailycount']):
        publish_date =datetime(today.year, today.month, today.day+1, 20, 15)

    else:

        publish_date = datetime(today.year, today.month+int(int(i)/30), today.day+1+int(int(i)/int(setting['dailycount'])), 20, 15)
    scheduletopublish_tomorrow(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])
    scheduletopublish_7dayslater(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])
    scheduletopublish_specific_date(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])

    #here we use video filename as video title, 
    # in the later gui you can set title prefix/suffix added to filename,des prefix/suffix added to prefer description for channel
    # and also tags too