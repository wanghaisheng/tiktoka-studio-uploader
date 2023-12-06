from upgenius.youtube.youtube_upload import YoutubeUpload
from datetime import datetime, date, timedelta
import asyncio
import os
import calendar

##prepare video and thumbnail with the same filename in pair, for example,
# -1.mp4
# -1.jpg
# -2.mp4
# -2.png


VIDEO_EXTENSIONS = (
    ".avi",
    ".divx",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpg",
    ".wmv",
)



CHANNEL_COOKIES = r"D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader\fastlane-cookie.json"
videopath = r"D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader\tests"
proxy_option = "socks5://127.0.0.1:1080"
prefertags = []

title = "bababala"
title = title[:95]
username = "edwin.uestc@gmail.com"
password = "U437P8Is9prmNquVerHJ9%R00bn"
description = "========================balabala"
scheduleTimeSlots = [
    "00:00",
    "00:15",
    "00:30",
    "00:45",
    "01:00",
    "01:15",
    "01:30",
    "01:45",
    "02:00",
    "02:15",
    "02:30",
    "02:45",
    "03:00",
    "03:15",
    "03:30",
    "03:45",
    "04:00",
    "04:15",
    "04:30",
    "04:45",
    "05:00",
    "05:15",
    "05:30",
    "05:45",
    "06:00",
    "06:15",
    "06:30",
    "06:45",
    "07:00",
    "07:15",
    "07:30",
    "07:45",
    "08:00",
    "08:15",
    "08:30",
    "08:45",
    "09:00",
    "09:15",
    "09:30",
    "09:45",
    "10:00",
    "10:15",
    "10:30",
    "10:45",
    "11:00",
    "11:15",
    "11:30",
    "11:45",
    "12:00",
    "12:15",
    "12:30",
    "12:45",
    "13:00",
    "13:15",
    "13:30",
    "13:45",
    "14:00",
    "14:15",
    "14:30",
    "14:45",
    "15:00",
    "15:15",
    "15:30",
    "15:45",
    "16:00",
    "16:15",
    "16:30",
    "16:45",
    "17:00",
    "17:15",
    "17:30",
    "17:45",
    "18:00",
    "18:15",
    "18:30",
    "18:45",
    "19:00",
    "19:15",
    "19:30",
    "19:45",
    "20:00",
    "20:15",
    "20:30",
    "20:45",
    "21:00",
    "21:15",
    "21:30",
    "21:45",
    "22:00",
    "22:15",
    "22:30",
    "22:45",
    "23:00",
    "23:15",
    "23:30",
    "23:45",
]

closewhen100percent = 0
# 0-wait uploading done
# 1-wait Processing done
# 2-wait Checking done


# auto install requirments for user
# checkRequirments()
upload = YoutubeUpload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    root_profile_directory="",
    proxy_option=proxy_option,
    headless=False,
    debug=True,
    use_stealth_js=False,
    # if you want to silent background running, set watcheveryuploadstep false
    CHANNEL_COOKIES=CHANNEL_COOKIES,
    username=username,
    browserType="firefox",
    closewhen100percent="go next after copyright check success",
    password=password,
    recordvideo=True
    # for test purpose we need to check the video step by step ,
)
today = date.today()
publish_date = ""
setting = {}
setting["dailycount"] = 4



def scheduletopublish_specific_date(videopath, thumbpath, filename, publish_date):
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    # publish_date = datetime(today.year, today.month, today.day, 10, 15)
    # if you want tomorrow ,just change 7 to 1
    # publish_date += timedelta(days=3)
    # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
    asyncio.run(
        upload.upload(
            videopath,
            title=filename[:95],
            description=description,
            thumbnail=thumbpath,
            tags=prefertags,
            closewhen100percentupload=True,
            publishpolicy=2,
            publish_date=publish_date,
        )
    )


load video json meta


videocount = len(videofiles)
maxdays = calendar._monthlen(today.year, today.month)
print("max day in  month", maxdays)
for i in range(videocount):
    monthoffset = int(int(i) / maxdays)
    startingday = today.day
    dayoffset = int(int(i) / int(setting["dailycount"]))
    if today.day + dayoffset + 1 > maxdays:
        monthoffset = 1
        startingday = today.day + dayoffset + 1 - maxdays
    print("di jige", i, " yuji fabu sjian", dayoffset)
    publish_date = datetime(
        today.year, today.month + monthoffset, startingday + 1 + dayoffset, 20, 15
    )

    date_to_post = publish_date.strftime("%b %d, %Y")
    print("=====date_to_post===", date_to_post)
    publish_date_str = publish_date.strftime("%Y-%m-%d %H:%M:%S")
    publish_date = datetime.fromisoformat(publish_date_str)
    date_to_post = publish_date.strftime("%b %d, %Y")

    print("=====date_to_post===", date_to_post)

    # scheduletopublish_tomorrow(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])
    # scheduletopublish_7dayslater(videofiles[i]['videopath'],videofiles[i]['thumbpath'],videofiles[i]['filename'])

    print(videofiles[i]["videopath"].split(os.sep)[-1], " is progress=========")
    scheduletopublish_specific_date(
        videofiles[i]["videopath"],
        videofiles[i]["thumbpath"],
        videofiles[i]["filename"],
        publish_date,
    )
    with open("done.txt", "a", encoding="utf8") as f:
        f.write("\r" + videofiles[i]["videopath"].split(os.sep)[-1] + "\r")
        f.close()
    # here we use video filename as video title,
    # in the later gui you can set title prefix/suffix added to filename,des prefix/suffix added to prefer description for channel
    # and also tags too
