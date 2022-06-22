from ytb_up.youtube import *
from datetime import datetime,date,timedelta
import asyncio
import os
import calendar
##prepare video and thumbnail with the same filename in pair, for example, 
# -1.mp4 
# -1.jpg
# -2.mp4
# -2.png


VIDEO_EXTENSIONS = ('.avi',
                    '.divx',
                    '.flv',
                    '.m4v',
                    '.mkv',
                    '.mov',
                    '.mp4',
                    '.mpg',
                    '.wmv')
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

                        for image_ext in ('.jpeg', '.png','.webp', '.jpg'):
                            videopath = os.path.join(r, entry.name)
                            thumbpath = os.path.join(r, filename+image_ext)
                            title=''
                            with open(folder+os.sep+filename+'.description','r',encoding='utf8') as f:
                                title=f.read()
                            
                            if os.path.exists(thumbpath):     
                                video={
                                "thumbpath":thumbpath,
                                "videopath":videopath,
                                "filename":title

                                }  
                                videofiles.append(video)                 

                                # print('========',videopath)
                                # print('========',thumbpath)

        # for dirs in d:
        #     print(dirs)  
        #     check_video_thumb_pair_basic(dirs)
    return videofiles



profilepath = ''
CHANNEL_COOKIES = r'D:\Download\audio-visual\saas\capcut\tiktok-videos\cookie.json'
CHANNEL_COOKIES=r'D:\Download\audio-visual\make-text-video\reddit-to-video\assets\cookies\aww.json'
videofolder = r'D:\Download\audio-visual\saas\capcut\tiktok-videos\videos'
prefertags = []
publish_date = ''
proxy_option = "socks5://127.0.0.1:1080"
username = "antivte"
password = ""
description = """
========================
Here is the CapCut University
 
CapCut is one of the most popular video editing apps for iPhone & Android right now. While it is from the same company behind TikTok (ByteDance), it’s not JUST a TikTok video editor - you can easily use it to create great videos on your smartphone for YouTube, Facebook, or any other use case!





Are you looking for a free video editing tool? This channel will teach you how to edit videos using the free mobile app, CapCut. Many people use the app to edit videos for TikTok, but the opportunities are endless! We will outline most of the more popular and essential features. These range from basic editing tricks, including how to navigate the app, to more unique features such as adding background music and filters.

"""
#you can set prefered description

upload = YoutubeUpload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    root_profile_directory='',
    proxy_option=proxy_option,
    watcheveryuploadstep=True,
    CHANNEL_COOKIES=CHANNEL_COOKIES,
    username=username,
    password=password,
    recordvideo=True
    
)
today = date.today()
publish_date=''
setting={}
setting['dailycount']=4

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



def scheduletopublish_specific_date(videopath,thumbpath,filename,publish_date):
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         
    # publish_date = datetime(today.year, today.month, today.day, 10, 15)
    #if you want tomorrow ,just change 7 to 1
    # publish_date += timedelta(days=3)
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
maxdays=calendar._monthlen(today.year, today.month)

for i in range(videocount):
    monthoffset=int(int(i)/maxdays)
    startingday=today.day
    dayoffset=int(int(i)/int(setting['dailycount']))
    if today.day+1>maxdays:
        monthoffset=1
        startingday=today.day+1-maxdays
    publish_date =datetime(today.year, today.month+monthoffset, startingday+1+dayoffset, 20, 15)


    # scheduletopublish_tomorrow(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])
    # scheduletopublish_7dayslater(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])
    data=[]
    if os.path.exists('done.txt') and os.path.getsize('done.txt')>0:
        with open('done.txt','r',encoding='utf8') as fr:
            data=fr.readlines()
            fr.close()
    else:
        with open('done.txt','a',encoding='utf8') as f:
            f.write('')        
            f.close()
    print(videofiles[i]['videopath'],' in queue=========',data)

    if not videofiles[i]['videopath'].split(os.sep)[-1] in data:
        print(videofiles[i]['videopath'],' is progress=========')            
        scheduletopublish_specific_date(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'],publish_date)
        with open('done.txt','a',encoding='utf8') as f:
            f.write(videofiles[i]['videopath'].split(os.sep)[-1]+'\r')
            f.close()
    #here we use video filename as video title, 
    # in the later gui you can set title prefix/suffix added to filename,des prefix/suffix added to prefer description for channel
    # and also tags too