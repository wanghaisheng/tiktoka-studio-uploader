from base64 import encode
from tsup.youtube import *
from datetime import datetime, date, timedelta
import asyncio
import os
import calendar
import pandas as pd
import sys
from autothumb import AiThumbnailGenerator

from threading import Lock
from threading import Condition
from concurrent.futures import ThreadPoolExecutor


##prepare excel


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


def choosefixipchannel(accountexcel):
    if accountexcel and os.path.exists(accountexcel):
        sheet = pd.read_excel(accountexcel, engine="openpyxl")
        my_dic = pd.read_excel(accountexcel, engine="openpyxl", index_col=None)

        for name in my_dic.iterrows():
            # print(name)
            item = name[1].to_dict()
            account = {}
            account["cookiepath"] = item["cookie"]
            account["ip"] = item["ip"]
            accounts.append(account)
        return accounts


def chooserandomchannel(cookiefolder, quanju_proxy):
    accounts = []

    for r, d, f in os.walk(cookiefolder):
        with os.scandir(r) as i:
            print("detecting----------", r)

            pairedvideothumbs = []
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    print(filename, "==", ext)

                    start_index = 0
                    if ext in (".json"):
                        cookiepath = os.path.join(r, entry.name)
                        # cookies.append(cookiepath)
                        account = {}
                        account["cookiepath"] = os.path.join(r, entry.name)
                        if quanju_proxy:
                            account["ip"] = ""
                        else:
                            account["ip"] = "socks5://127.0.0.1:1080"
                        accounts.append(account)
    return accounts


def check_video_thumb_pair(excelpath):
    # print('detecting----------',folder)
    videofiles = []
    data = []
    if os.path.exists("done.txt") and os.path.getsize("done.txt") > 0:
        with open("done.txt", "r", encoding="utf8") as fr:
            data = fr.readlines()
            fr.close()
    else:
        with open("done.txt", "a", encoding="utf8") as f:
            f.write("")
            f.close()
    data = [x.replace("\n", "") for x in data]
    print("done videos ", len(data))
    # sheet=pd.read_excel(excelpath, encoding=sys.getfilesystemencoding())

    sheet = pd.read_excel(excelpath, engine="openpyxl")
    my_dic = pd.read_excel(excelpath, engine="openpyxl", index_col=None)

    for name in my_dic.iterrows():
        # print(name)
        item = name[1].to_dict()
        video = {}
        video["videopath"] = item["video/project"]
        video["title"] = item["title/target name"]
        video["category"] = item["category"]
        video["description"] = item["description"]
        video["tags"] = item["tags"]
        video["thumbpath"] = ""
        video["publishpolicy"] = item["privacy"]
        videofiles.append(video)
    return videofiles


def list_split(items, n):
    return [items[i : i + n] for i in range(0, len(items), n)]


accounts = []

profilepath = ""
# CHANNEL_COOKIES = r'D:\Download\audio-visual\saas\capcut\tiktok-videos\cookie.json'
prefertags = []
publish_date = ""
proxy_option = "socks5://127.0.0.1:1080"
# proxy_option = ""
username = "antivte"
password = ""
setting = {}

# =================下面的几个参数需要你自行按照需要修改
excelpath = "youtube.xlsx"

# 每个频道每天公开视频数量上限 目前手动设置为4
setting["dailycount"] = 50
# 1 表示从明天开始公开 0 表示从今天开始公开 7 表示从一周以后开始公开
initialday = 0
# 默认是早上10点15分开始发布 但你运行程序的时间可能是11点15 那就需要你按情况修改下面的小时 分钟的数值
initialhour = 10
initialminute = 15
# 每个频道每天上传视频数量上限 目前手动设置为20
maxchanneldailypublishcount = 50
# 所有同类型频道的cookie放在这个文件夹下面，每个频道每天传20个就切换一下
cookiefolder = "./cookies"
# cookiefolder = r'D:\Download\audio-visual\saas\capcut\tiktok-videos\cookies'

accountexcel = ""
# 浏览器静默运行 如果是调试过程请设置为False
silent = True
# 是否设置为全局代理
quanju_proxy = False
# =================上面的几个参数需要你自行按照需要修改


videoallfiles = check_video_thumb_pair(excelpath)
t = list_split(videoallfiles, maxchanneldailypublishcount)
if os.path.exists(accountexcel):
    accounts = choosefixipchannel(accountexcel)
else:
    accounts = chooserandomchannel(cookiefolder, quanju_proxy)

if len(videoallfiles) < maxchanneldailypublishcount:
    t[0] = videoallfiles
if len(accounts) > 0:
    for i in range(len(t)):
        videofiles = t[i]
        videocount = len(videofiles)
        print("count queue", videocount)
        print("当前帐号信息是", accounts[i])
        today = date.today()
        publish_date = ""
        if "ip" in accounts[i]:
            proxy_option = accounts[i]["ip"]
            cookiepath = accounts[i]["cookiepath"]
        print("当前cookie是", cookiepath)
        print("当前服务器是", proxy_option)

        upload = YoutubeUpload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            root_profile_directory="",
            proxy_option=proxy_option,
            watcheveryuploadstep=silent,
            CHANNEL_COOKIES=cookiepath,
            username=username,
            password=password,
            recordvideo=True,
        )

        def scheduletopublish_specific_date(
            videopath,
            thumbpath,
            title,
            description,
            category,
            publish_date,
            prefertags,
            return_dict,
            retry=3,
        ):
            # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
            # mode b:release_offset not exist, publishdate exist , schedule to this specific date
            # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
            # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
            # publish_date = datetime(today.year, today.month, today.day, 10, 15)
            # if you want tomorrow ,just change 7 to 1
            # publish_date += timedelta(days=3)
            # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")

            # 每个video至多尝试upload三次
            while retry:
                try:
                    res, videoid = asyncio.run(
                        upload.upload(
                            videopath,
                            title=title[:95],
                            description=description,
                            thumbnail=thumbpath,
                            tags=prefertags,
                            closewhen100percentupload=True,
                            publishpolicy=2,
                            publish_date=publish_date,
                        )
                    )

                    return_dict[videopath] = videoid
                    return videoid

                except:
                    retry -= 1

                    return_dict[videopath] = False
                    return False

        # task done callback that will re-submit failed tasks
        def auto_retry(future):
            global executor, futures_to_data, tasks_completed
            # check for a failure
            if future.exception():
                # get the associated data for the task
                data = futures_to_data[future]
                # re-submit the task
                retry = executor.submit(scheduletopublish_specific_date, data)
                # add to the map
                futures_to_data[retry] = data
                # add the callback
                retry.add_done_callback(auto_retry)
                # report the failure
                print(f"Failure, retrying {data}")
            else:
                # report success
                print("jieguo===", future.result())
                # update the count of completed tasks
                with lock:
                    tasks_completed += 1
                    if tasks_completed >= TASKS:
                        with condition:
                            condition.notify()

        maxdays = calendar._monthlen(today.year, today.month)
        print("max day in  month", maxdays)
        for i in range(videocount):
            print("======\r", videofiles[i])

            monthoffset = int(int(i) / maxdays)
            startingday = today.day
            dayoffset = int(int(i) / int(setting["dailycount"]))
            if today.day + dayoffset + 1 > maxdays:
                monthoffset = 1
                startingday = today.day + dayoffset - maxdays
            publish_date = datetime(
                today.year,
                today.month + monthoffset,
                startingday + initialday + dayoffset,
                initialhour,
                initialminute,
            )
            date_to_post = publish_date.strftime("%b %d, %Y")
            print("=====date_to_post===", date_to_post)
            publish_date_str = publish_date.strftime("%Y-%m-%d %H:%M:%S")
            if not "publish_date" in videofiles[i]:
                videofiles[i]["publish_date"] = publish_date_str
            else:
                if (
                    videofiles[i]["publish_date"] == ""
                    or videofiles[i]["publish_date"] is None
                ):
                    videofiles[i]["publish_date"] = publish_date_str
            print("设置的发布时间为", videofiles[i]["publish_date"])
            if not "thumbpath" in videofiles[i]:
                thumbpath = AiThumbnailGenerator(videofiles[i]["videopath"])
                videofiles[i]["thumbpath"] = videofiles[i]["videopath"].replace(
                    ".mp4", "-1.jpg"
                )

                print("generated thumbnail is", thumbpath)
            else:
                if (
                    videofiles[i]["thumbpath"] == ""
                    or videofiles[i]["thumbpath"] is None
                ):
                    # create_thumbnail(videofiles[i]['videopath'])
                    # Katna
                    thumbpath = AiThumbnailGenerator(videofiles[i]["videopath"])
                    videofiles[i]["thumbpath"] = videofiles[i]["videopath"].replace(
                        ".mp4", "-1.jpg"
                    )
                    print("generated thumbnail is", thumbpath)

            # constant defining the total tasks to complete
            TASKS = 1
            # count of tasks that are completed
            tasks_completed = 0
            # lock protecting the count of completed tasks
            lock = Lock()
            condition = Condition()
            # create a thread pool

            # from multiprocessing import Manager
            # manager=Manager()
            # statusdata=manager.dict()
            statusdata = dict()
            with ThreadPoolExecutor(TASKS) as executor:
                # submit ten tasks
                futures_to_data = {
                    executor.submit(
                        lambda p: scheduletopublish_specific_date(*p),
                        [
                            videofiles[i]["videopath"],
                            videofiles[i]["thumbpath"],
                            videofiles[i]["title"],
                            videofiles[i]["description"],
                            "",
                            videofiles[i]["publish_date"],
                            videofiles[i]["tags"],
                            statusdata,
                        ],
                    ): i
                    for i in range(TASKS)
                }
                # register callbacks
                # for future in as_completed(futures_to_data):
                # for future in futures_to_data:
                # future.add_done_callback(auto_retry)
                # block, wait for all tasks to be completed successfully
                with condition:
                    condition.wait()
                    print("running==========", statusdata)

                    print("正在尝试上传文件...", videofiles[i]["videopath"])

                    with open("done.txt", "a", encoding="utf8") as f:
                        f.write(
                            "\r" + videofiles[i]["videopath"].split(os.sep)[-1] + "\r"
                        )
                        f.close()

                    with open("undone.txt", "a", encoding="utf8") as f:
                        f.write(
                            "\r" + videofiles[i]["videopath"].split(os.sep)[-1] + "\r"
                        )
                        f.close()


else:
    print("没有找到channel对应的cookie")


# https://imciel.com/2020/08/27/create-custom-tunnel/
