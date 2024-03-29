"""
Uploads multiple videos downloaded from the internet
"""
from upgenius.tiktok.selenium.TikTokAdspowerUploader import AdspowerUploader
from upgenius.tiktok.selenium.auth import AuthBackend


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

    uploader = AdspowerUploader("jie", "new bag.mp4", "conf.json", None)
    uploader.upload()
