from base64 import encode
from ytb_up.youtube import *
from datetime import datetime,date,timedelta
import asyncio
import os
import calendar
import pandas as pd
import sys
from autothumb import AiThumbnailGenerator

##prepare excel

## install pyav
## pip install av

VIDEO_EXTENSIONS = ('.avi',
                    '.divx',
                    '.flv',
                    '.m4v',
                    '.mkv',
                    '.mov',
                    '.mp4',
                    '.mpg',
                    '.wmv')
def choosechannel(cookiefolder):
    cookies=[]

    for r, d, f in os.walk(cookiefolder):
        with os.scandir(r) as i:
            print('detecting----------',r)

            pairedvideothumbs=[]
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    print(filename,'==',ext) 

                    start_index=0
                    if ext in ('.json'):
                        cookiepath = os.path.join(r, entry.name)
                        cookies.append(cookiepath)
    return cookies
def check_video_thumb_pair(excelpath):
    # print('detecting----------',folder)
    videofiles = []
    data=[]
    if os.path.exists('done.txt') and os.path.getsize('done.txt')>0:
        with open('done.txt','r',encoding='utf8') as fr:
            data=fr.readlines()
            fr.close()
    else:
        with open('done.txt','a',encoding='utf8') as f:
            f.write('')        
            f.close()
    data=[x.replace('\n','') for x in data]
    print('done videos ',len(data))
    # sheet=pd.read_excel(excelpath, encoding=sys.getfilesystemencoding())

    sheet=pd.read_excel(excelpath, engine='openpyxl')
    my_dic = pd.read_excel(excelpath, engine='openpyxl', index_col=None)

    for name in my_dic.iterrows():
        # print(name)
        item=name[1].to_dict()
        video={}
        video['videopath']=item['video/project']
        video['title']=item['title/target name']
        video['category']=item['category']
        video['description']=item['description']
        video['tags']=item['tags']
        video['thumbpath']=''
        video['publishpolicy']=item['privacy']
        videofiles.append(video)
    return videofiles


def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]


profilepath = ''
# CHANNEL_COOKIES = r'D:\Download\audio-visual\saas\capcut\tiktok-videos\cookie.json'
prefertags = []
publish_date = ''
proxy_option = "socks5://127.0.0.1:1080"
username = "antivte"
password = ""
setting={}

#=================下面的几个参数需要你自行按照需要修改
excelpath='youtube视频批量上传.xlsx'

#每个频道每天公开视频数量上限 目前手动设置为4
setting['dailycount']=4
# 1 表示从明天开始公开 0 表示从今天开始公开 7 表示从一周以后开始公开
initialday=0
#每个频道每天上传视频数量上限 目前手动设置为20
maxchanneldailypublishcount=20
#所有同类型频道的cookie放在这个文件夹下面，每个频道每天传20个就切换一下
cookiefolder=r'D:\Download\audio-visual\saas\capcut\tiktok-videos\cookies'

#=================上面的几个参数需要你自行按照需要修改


videoallfiles=check_video_thumb_pair(excelpath)
t =list_split(videoallfiles,maxchanneldailypublishcount)
cookies=choosechannel(cookiefolder)
if len(videoallfiles)<maxchanneldailypublishcount:
    t[0]=videoallfiles
if len(cookies)>0:

    for i in range(len(t)):
        videofiles=t[i]
        videocount=len(videofiles)
        print('count queue',videocount)

        today = date.today()
        publish_date=''


        upload = YoutubeUpload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            root_profile_directory='',
            proxy_option=proxy_option,
            watcheveryuploadstep=True,
            CHANNEL_COOKIES=cookies[i],
            username=username,
            password=password,
            recordvideo=True
            
        )
        def scheduletopublish_specific_date(videopath,thumbpath,title,description,category,publish_date,prefertags):
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
                title=title[:95],
                description=description,
                thumbnail=thumbpath,
                tags=prefertags,
                closewhen100percentupload=True,
                publishpolicy=2,
                publish_date=publish_date

            ))



        maxdays=calendar._monthlen(today.year, today.month)
        print('max day in  month',maxdays)
        for i in range(videocount):
            print('======\r',videofiles[i])

            monthoffset=int(int(i)/maxdays)
            startingday=today.day
            dayoffset=int(int(i)/int(setting['dailycount']))
            if today.day+dayoffset+1>maxdays:
                monthoffset=1
                startingday=today.day+dayoffset-maxdays
            if 'publish_date' in videofiles[i]:
                if videofiles[i]['publish_date']=='' or videofiles[i]['publish_date'] is None:
                    publish_date =datetime(today.year, today.month+monthoffset, startingday+dayoffset, 20, 15)
                    publish_date += timedelta(days=initialday)
            if not 'thumbpath' in videofiles[i]:
                thumbpath = AiThumbnailGenerator(videofiles[i]['videopath'])
                videofiles[i]['thumbpath']=thumbpath
                print('generated thumbnail is', thumbpath)
            else:
                if videofiles[i]['thumbpath']=='' or videofiles[i]['thumbpath'] is None:
                    # create_thumbnail(videofiles[i]['videopath'])
                    # Katna
                    thumbpath = AiThumbnailGenerator(videofiles[i]['videopath'])
                    videofiles[i]['thumbpath']=thumbpath
                    print('generated thumbnail is', thumbpath)
            scheduletopublish_specific_date(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['title'],videofiles[i]['description'],'',publish_date,videofiles[i]['tags'])
            with open('done.txt','a',encoding='utf8') as f:
                f.write('\r'+videofiles[i]['videopath'].split(os.sep)[-1]+'\r')
                f.close()
else:
    print('没有找到channel对应的cookie')