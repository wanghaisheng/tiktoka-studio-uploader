import os
import re
import sys

sys.path.insert(0, re.sub(r"([\\/]items$)|([\\/]spiders$)", "", os.getcwd()))

__all__ = [
    "AirSpider",
    "Spider",
    "TaskSpider",
    "BatchSpider",
    "BaseParser",
    "TaskParser",
    "BatchParser",
    "Request",
    "Response",
    "Item",
    "UpdateItem",
    "ArgumentParser",
]

from upgenius.utils.exceptions import *
from upgenius.utils.constants import *
from upgenius.utils.log import Log
from upgenius.youtube.youtube_upload import YoutubeUpload
from upgenius.tiktok.sessionId.uploader import upload2TiktokSessionId

from upgenius.douyin.douyin_upload import DouyinUpload

# from upgenius.login import *
# from upgenius.db import *
# from upgenius.tiktok import *
from upgenius.utils.custom_argparse import ArgumentParser