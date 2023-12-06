from upgenius.youtube.youtube_upload import YoutubeUpload
from datetime import datetime, date, timedelta
import asyncio
from upgenius.utils.webdriver.setupPL import checkRequirments
from upgenius.youtube.youtube_helper import LOG_LEVEL,BROWSER_TYPE,WAIT_POLICY

import os
# If it is the first time you've run the utility, a browser window should popup and prompt you to provide Youtube credentials. A token will be created and stored in request.token file in the local directory for subsequent use.

profilepath = (
    r"D:\Download\audio-visual\make-text-video\reddit-to-video\assets\profile\fastlane"
)
channel_cookie_path =r"/Users/wenke/github/tiktoka-studio-uploader/offloaddogsboner-cookie.json"



videopath =r"/Users/wenke/github/tiktoka-studio-uploader/tests/1.mp4"
tags = ["ba,baaa,bababa"]
date_to_publish = ""
# if you use some kinda of proxy to access youtube,
proxy_option = "socks5://127.0.0.1:1080"

# for cookie issue,
video_title = "bababala"
video_title = video_title[:95]
username = "edwin.uestc@gmail.com"
password = "U437P8Is9prmNquVerHJ9%R00bn"
video_description = "========================balabala"
invalid_thumbnail = r"D:\Download\audio-visual\make-reddit-video\reddit-to-video\assets\ace\ace-attorney_feature.jpg"
thumbnail_local_path = r"/Users/wenke/github/tiktoka-studio-uploader/tests/1/sp/1-001.jpg"


closewhen100percent = 0
# 0-wait uploading done
# 1-wait Processing done
# 2-wait Checking done
def checkfilebroken(path):
    print(f"check whether file exist{path}")
    if (os.path.exists(path)
        and os.path.getsize(path) > 0
    ):
        print(f'{path} is exist')
        return True
    else:
        print(f'{path} is not  exist')

        return False


# auto install requirments for user
# checkRequirments()
upload = YoutubeUpload(
    # use r"" for paths, this will not give formatting errors e.g. "\n"
    profile_directory=None,
    proxy_option=proxy_option,
    is_open_browser=False,
    log_level=LOG_LEVEL.DEBUG,
    use_stealth_js=False,
    # if you want to silent background running, set watcheveryuploadstep false
    channel_cookie_path=channel_cookie_path,
    username=username,
    browser_type=BROWSER_TYPE.FIREFOX,
    wait_policy=WAIT_POLICY.GO_NEXT_UPLOAD_SUCCESS,
    password=password,
    is_record_video=True
    # for test purpose we need to check the video step by step ,
)
today = date.today()


def instantpublish():
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="instant publish-test-005",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=1,
        )
    )

def unlistedpublish():
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="unlisted public publish-test-005",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=3,
        )
    )

def premierepublish():
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="premiere public publish-test-005",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=4,
        )
    )


def saveasprivatedraft():
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="private draft-test-004",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=0,
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
    #         video_title="tomorrow-test-001",
    #         video_description=video_description,
    #         thumbnail_local_path=thumbnail_local_path,
    #         tags=tags,
    #         publishpolicy=2,
    #         date_to_publish=date_to_publish,
    #         hour_to_publish=hour_to_publish,
    #     )
    # )
    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="tomorrow-test-001",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=2,
            release_date=date_to_publish,
            release_date_hour=hour_to_publish,
        )
    )


def scheduletopublish_every7days():
    # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
    # mode b:release_offset not exist, publishdate exist , schedule to this specific date
    # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
    # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
    date_to_publish = datetime(today.year, today.month, today.day)
    hour_to_publish = "17:15"
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    date_to_publish += timedelta(days=7)
    # hour_to_publish=datetime.strptime(hour_to_publish, "%H:%M")

    # print('after convert',hour_to_publish.strftime("%I:%M %p").strip("0"))

    asyncio.run(
        upload.upload(
            video_local_path=videopath,
            video_title="7days later-test-003",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=2,
            release_date=date_to_publish,
            release_date_hour=hour_to_publish,
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
            video_local_path=videopath,
            video_title="four days later-test-002",
            video_description=video_description,
            thumbnail_local_path=thumbnail_local_path,
            tags=tags,
            publish_policy=2,
            release_date=date_to_publish,
            release_date_hour=hour_to_publish,
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

checkfilebroken(channel_cookie_path)
checkfilebroken(thumbnail_local_path)
checkfilebroken(videopath)


checkRequirments()
unlistedpublish()
premierepublish()

# scheduletopublish_tomorrow()
# scheduletopublish_at_specific_date()
# scheduletopublish_every7days()
# saveasprivatedraft()
# instantpublish()
# friststart()
