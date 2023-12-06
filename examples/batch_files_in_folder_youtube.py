from upgenius.youtube.youtube_upload import YoutubeUpload
from upgenius.youtube.models.youtube_models import YoutubeVideo,UploadSetting

from datetime import datetime, date, timedelta
import asyncio
import os
import calendar

##prepare video and thumbnail with the same filename in pair, for example,
# -1.mp4
# -1.jpg
# -2.mp4
# -2.png


VIDEO_EXTENSIONS = [
    ".avi",
    ".divx",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpg",
    ".wmv",
]


def analyse_video_thumb_pair(folder):
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
    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            print("detecting----------", r)

            pairedvideothumbs = []
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    # print(filename,'==',ext)

                    start_index = 0
                    if ext in VIDEO_EXTENSIONS:
                        # if ext in ('.flv', '.mp4', '.avi'):

                        for image_ext in (".jpeg", ".png", ".webp", ".jpg"):
                            videopath = os.path.join(r, entry.name)
                            thumbpath = os.path.join(r, filename + image_ext)
                            title = ""
                            with open(
                                folder + os.sep + filename + ".description",
                                "r",
                                encoding="utf8",
                            ) as f:
                                title = f.read()

                            if os.path.exists(thumbpath):

                                video = YoutubeVideo(
                                    video_local_path=videopath,
                                    video_title=title,
                                    video_ext=ext,
                                    thumbnail_locapath=thumbpath
                                    )


                                if not videopath.split(os.sep)[-1] in data:
                                    videofiles.append(video)

                                # print('========',videopath)
                                # print('========',thumbpath)

        # for dirs in d:
        #     print(dirs)
        #     check_video_thumb_pair_basic(dirs)
    return videofiles






# scan video files
# prepare youtube video metas
videofolder = r"D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader\tests"

videofiles = analyse_video_thumb_pair(videofolder)
## parse meta from video file
prefertags = ['tiktoka studio']

today = date.today()
publish_date = ""
setting = {}
setting["dailycount"] = 4

maxdays = calendar._monthlen(today.year, today.month)
print("max day in  month", maxdays)
for i,video in enumerate(videofiles):
## auto gen publish date

    monthoffset = int(int(i) / maxdays)
    startingday = today.day
    dayoffset = int(int(i) / int(setting["dailycount"]))
    if today.day + dayoffset + 1 > maxdays:
        monthoffset = 1
        startingday = today.day + dayoffset + 1 - maxdays
    publish_date = datetime(
        today.year, today.month + monthoffset, startingday + 1 + dayoffset, 20, 15
    )

    date_to_post = publish_date.strftime("%b %d, %Y")
    print("=====date_to_post===", date_to_post)
    publish_date_str = publish_date.strftime("%Y-%m-%d %H:%M:%S")
    publish_date = datetime.fromisoformat(publish_date_str)

    print("=====date_to_post===", date_to_post)
    date_to_post = publish_date.strftime("%b %d, %Y")
    video.publish_policy=2
## manual set each field

    video.upload_date=today
    video.release_date=publish_date
    video.release_date_hour_to_publish="15:30"
    video.tags=prefertags
# save/read video metas to/from excel/json/sqlite

# auto install requirments for user
# checkRequirments()
# for cookie issue,
CHANNEL_COOKIES = r"D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader\fastlane-cookie.json"
proxy_option = "socks5://127.0.0.1:1080"


username = "edwin.uestc@gmail.com"
password = "U437P8Is9prmNquVerHJ9%R00bn"

closewhen100percent = 0
# 0-wait uploading done
# 1-wait Processing done
# 2-wait Checking done
uploadSetting=UploadSetting(
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
    recordvideo=True)



upload = YoutubeUpload(uploadSetting)


asyncio.run(
    upload.upload(
        video.video_local_path,
        title=video.video_title,
        description=video.video_description,
        thumbnail=video.thumbnail_locapath,
        tags=video.tags,
        publishpolicy=2,
        publish_date=video.release_date,
    )
)

