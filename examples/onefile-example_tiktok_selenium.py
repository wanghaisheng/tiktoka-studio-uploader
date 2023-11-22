"""
Uploads multiple videos downloaded from the internet
"""
from tsup.tiktok.selenium.uploader import upload_videos
from tsup.tiktok.selenium.auth import AuthBackend

FILENAME = "upload.mp4"

# max limit: 10 days later than now
schedule = datetime.datetime(2023, 12, 20, 13, 00)

videos = [
    {
        "path": "upload.mp4",
        "description": "This is the first upload"
    },
    {
        "path": "upload.mp4",
        "schedule": schedule,
        "description": "This is video with hashtag and mentions #fyp @icespicee"
    }
]

if __name__ == "__main__":
    
    
    
# # proxy = {'user': 'myuser', 'pass': 'mypass', 'host': '111.111.111', 'port': '99'}  # user:pass
# proxy = {'host': '111.111.111', 'port': '99'}
# upload_video(..., proxy=proxy)    
    # authentication backend
    # you can use cookie.json or cookie.txt from browser extension
    
    # you can use our script to save one
    
    # python examples/save-tiktok-Cookie.py
    # auth = AuthBackend(cookies="cookies.txt")
    auth = AuthBackend(cookies="cookies.json")

    # upload video to TikTok
    upload_videos(videos, auth=auth)