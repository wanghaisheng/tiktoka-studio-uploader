"""
Uploads multiple videos downloaded from the internet
"""
from upgenius.tiktok.selenium.uploader import upload_videos
from upgenius.tiktok.selenium.auth import AuthBackend
from datetime import datetime, date, timedelta

FILENAME = "upload.mp4"
proxy = {'user': 'myuser', 'pass': 'mypass', 'host': '111.111.111', 'port': '99'}  # user:pass

# max limit: 10 days later than now
schedule = datetime(2023, 12, 20, 13, 00)
BROWSERS = [
    'chrome',
    'safari',
    'chromium',
    'edge',
    'firefox'
]

#  🫵 Mentions and Hashtags
# you should embed them in description field

onevideo = [
    {
        "path": "tests/1.mp4",
        "schedule": schedule,
        "description": "This is video with hashtag and mentions #fyp @icespicee"
    }
]
morevideos = [
    {
        "path": "tests/1.mp4",
        "description": "This is the first upload"
    },
    {
        "path": "tests/1.mp4",
        "schedule": schedule,
        "description": "This is video with hashtag and mentions #fyp @icespicee"
    }
]

if __name__ == "__main__":




    # authentication backend
    # you can use cookie.json or cookie.txt from browser extension

    # you can use our script to save one

    # python examples/save-tiktok-Cookie.py
    # cookie.txt exported from [Get cookies.txt LOCALLY] as descirbe here:docs\how-to-upload-tiktok.md
    # auth = AuthBackend(cookies="cookies.txt")
    auth = AuthBackend(cookies="tests/aww.json")


    # upload bulk videos to TikTok
    upload_videos(morevideos,
                  
            auth=auth,
            browser='chrome', 
            #  To set a proxy, currently only works with chrome as the browser
            proxy=proxy,
            # The datetime to schedule the video will be treated with the UTC timezone.
# The scheduled datetime must be at least 20 minutes in the future and a maximum of 10 days.
            schedule=schedule,
             #To set whether or not a video uploaded allows stitches, comments or duet,
             comment=True, stitch=True, duet=True,

             headless=True
             )
