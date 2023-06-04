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

from tsup.exceptions import *
from tsup.constants import *
from tsup.logging import Log
from tsup.youtube import YoutubeUpload
from tsup.douyin import DouyinUpload

# from tsup.login import *
# from tsup.db import *
# from tsup.tiktok import *
from tsup.utils.custom_argparse import ArgumentParser
from tsup.network.request import Request
from tsup.network.response import Response
from tsup.network.item import Item, UpdateItem
