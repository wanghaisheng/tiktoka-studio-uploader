from tsup.youtube.youtube_upload import YoutubeUpload
from datetime import datetime, date, timedelta
import asyncio
from tsup.utils.webdriver.setupPL import checkRequirments

profilepath = (
    r"D:\Download\audio-visual\make-text-video\reddit-to-video\assets\profile\fastlane"
)
CHANNEL_COOKIES = "../fastlane-cookie.json"

videopath = "../tests/1.mp4"
tags = ["ba,baaa,bababa"]
date_to_publish = ""
# if you use some kinda of proxy to access youtube,
proxy_option = "socks5://127.0.0.1:1080"

# for cookie issue,
title = "bababala"
title = title[:95]
username = "edwin.uestc@gmail.com"
password = "U437P8Is9prmNquVerHJ9%R00bn"
description = "========================balabala"
invalid_thumbnail = r"D:\Download\audio-visual\make-reddit-video\reddit-to-video\assets\ace\ace-attorney_feature.jpg"
thumbnail = r"D:\Download\audio-visual\saas\tiktoka\ytb-up\tests\1\sp\1-001.jpg"
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


def instantpublish():
    asyncio.run(
        upload.upload(
            videopath=videopath,
            title="instant publish-test-005",
            description=description,
            thumbnail=thumbnail,
            tags=tags,
            publishpolicy=1,
        )
    )


def saveasprivatedraft():
    asyncio.run(
        upload.upload(
            videopath=videopath,
            title="private draft-test-004",
            description=description,
            thumbnail=thumbnail,
            tags=tags,
            publishpolicy=0,
        )
    )


def scheduletopublish_tomorrow():
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=1)
    # asyncio.get_event_loop().run_until_complete(
    #     upload.upload(
    #         videopath=videopath,
    #         title="tomorrow-test-001",
    #         description=description,
    #         thumbnail=thumbnail,
    #         tags=tags,
    #         publishpolicy=2,
    #         date_to_publish=date_to_publish,
    #         hour_to_publish=hour_to_publish,
    #     )
    # )
    asyncio.run(
        upload.upload(
            videopath=videopath,
            title="tomorrow-test-001",
            description=description,
            thumbnail=thumbnail,
            tags=tags,
            publishpolicy=2,
            date_to_publish=date_to_publish,
            hour_to_publish=hour_to_publish,
        )
    )


def scheduletopublish_every7days():
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=7)
    # hour_to_publish=datetime.strptime(hour_to_publish, "%H:%M")

    # print('after convert',hour_to_publish.strftime("%I:%M %p").strip("0"))

    asyncio.run(
        upload.upload(
            videopath=videopath,
            title="7days later-test-003",
            description=description,
            thumbnail=thumbnail,
            tags=tags,
            publishpolicy=2,
            date_to_publish=date_to_publish,
            hour_to_publish=hour_to_publish,
        )
    )


def scheduletopublish_at_specific_date():
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "10:15"
    # if you want tomorrow ,just change 7 to 1
    date_to_publish += timedelta(days=3)
    # date_to_publish = datetime.strftime(date_to_publish, "%Y-%m-%d %H:%M:%S")
    asyncio.run(
        upload.upload(
            videopath=videopath,
            title="four days later-test-002",
            description=description,
            thumbnail=thumbnail,
            tags=tags,
            publishpolicy=2,
            date_to_publish=date_to_publish,
            hour_to_publish=hour_to_publish,
        )
    )
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
    #             if date_to_publish is None:
    #                 date_to_publish =datetime(
    #                     date.today().year,  date.today().month,  date.today().day, 10, 15)
    #             else:
    #                 date_to_publish += offset


scheduletopublish_tomorrow()
scheduletopublish_at_specific_date()
scheduletopublish_every7days()
saveasprivatedraft()
instantpublish()
# friststart()
