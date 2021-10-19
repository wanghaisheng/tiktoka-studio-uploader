from opplast import Upload
import os,json

import requests

from time import sleep
from datetime import datetime,date

def url_ok(url):


    try:
        response = requests.head(url)
    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        return False
    else:
        if response.status_code == 200:
            # print("OK")
            return True
        else:
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False
def load_setting():

    global setting
    try:
        print('读取配置文件', setting_file)

        fp = open(setting_file, 'r', encoding='utf-8')
        setting_json = fp.read()
        fp.close()
    except:
        print('读取配置文件失败 加载默认模版')
        fp = open("assets/config/setting-template.json", 'r', encoding='utf-8')
        setting_json = fp.read()
        fp.close()
    setting = json.loads(setting_json)
    print('当前使用的配置为：', setting)
    return setting


if __name__ == "__main__":
    videos=[]

    options = {
        'backend': 'mitmproxy',
        'proxy': {
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    print('checking whether need proxy setting')
    if url_ok('http://www.google.com'):
        print('network is fine,there is no need for proxy ')
        upload = Upload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            setting['firefox_profile_folder'],
            CHANNEL_COOKIES=setting['channelcookiepath']
        )
    else:
        print('we need for proxy ')

        upload = Upload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            setting['firefox_profile_folder'],
            proxy_option=options,
            headless=False,
            CHANNEL_COOKIES=setting['channelcookiepath']
        )
    print('preprare video metas')
    for video in videos:
        thumbpath = video["thumbpath"]
        des = video["des"]
        videopath = video["videopath"]
        tags = video["tags"]
        publish_date =video["publish_date"]
        publish_date = datetime.strptime(publish_date, "%Y-%m-%d %H:%M:%S")               
        title = video["title"]
        title = os.path.splitext(os.path.basename(title)[-1])[0]

        videoid=video['videoid']
        was_uploaded, upload_video_id = upload.upload(
            videopath,
            title=title,
            description=des,
            thumbnail=thumbpath,
            tags=tags.split(','),
            publish_date=publish_date
        )

        if was_uploaded:

            print(f"{videoid} has been uploaded to YouTube")

    upload.close()