import requests, json, time
from util import (
    assertSuccess,
    printError,
    getTagsExtra,
    uploadToTikTok,
    log,
    getCreationId,
)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"


def uploadVideo(session_id, video, title, tags, users=[]):
    session = requests.Session()

    session.cookies.set("sessionid", session_id, domain=".tiktok.com")
    session.verify = True
    headers = {"User-Agent": UA}
    url = "https://us.tiktok.com/upload/"
    r = session.get(url, headers=headers)
    if not assertSuccess(url, r):
        return False
    creationid = getCreationId()
    url = f"https://us.tiktok.com/api/v1/web/project/create/?creation_id={creationid}&type=1&aid=1988"
    headers = {"X-Secsdk-Csrf-Request": "1", "X-Secsdk-Csrf-Version": "1.2.8"}
    r = session.post(url, headers=headers)
    if not assertSuccess(url, r):
        return False
    tempInfo = r.json()["project"]
    creationID = tempInfo["creationID"]
    projectID = tempInfo["project_id"]
    # 获取账号信息
    url = "https://us.tiktok.com/passport/web/account/info/"
    r = session.get(url)
    if not assertSuccess(url, r):
        return False
    # user_id = r.json()["data"]["user_id_str"]
    log("开始上传视频")
    video_id = uploadToTikTok(video, session)
    if not video_id:
        log("视频上传失败")
        return False
    log("视频上传成功")
    time.sleep(2)
    result = getTagsExtra(title, tags, users, session)
    time.sleep(3)
    title = result[0]
    text_extra = result[1]
    url = "https://us.tiktok.com/api/v1/web/project/post/?aid=1988"
    data = {
        "upload_param": {
            "video_param": {"text": title, "text_extra": text_extra, "poster_delay": 0},
            "visibility_type": 0,
            "allow_comment": 1,
            "allow_duet": 0,
            "allow_stitch": 0,
            "sound_exemption": 0,
            "geofencing_regions": [],
            "creation_id": creationID,
            "is_uploaded_in_batch": False,
            "is_enable_playlist": False,
            "is_added_to_playlist": False,
        },
        "project_id": projectID,
        "draft": "",
        "single_upload_param": [],
        "video_id": video_id,
    }
    headers = {
        # "X-Secsdk-Csrf-Token": x_csrf_token,
        "Host": "us.tiktok.com",
        "authority": "tiktok.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "user-agent": UA,
        "sec-ch-ua-platform": '"macOS"',
        "origin": "https://www.tiktok.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.tiktok.com/",  # network find vn tiktok, referer: https://us.tiktok.com/creator
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    r = session.post(url, data=json.dumps(data), headers=headers)
    if not assertSuccess(url, r):
        log("发布失败")
        printError(url, r)
        return False
    if r.json()["status_code"] == 0:
        log("发布成功")
    else:
        log("发布失败")
        printError(url, r)
        return False

    return True


# if __name__ == "__main__":
# 	import argparse
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("-i", "--session_id", help="Tiktok sessionid cookie", required=True)
# 	parser.add_argument("-p", "--path", help="Path to video file", required=True)
# 	parser.add_argument("-t", "--title", help="Title of the video", required=True)
# 	parser.add_argument("--tags", nargs='*', default=[], help="List of hashtags for the video")
# 	parser.add_argument("--users", nargs='*', default=[], help="List of mentioned users for the video")
# 	parser.add_argument("-s", "--schedule_time", type=int, default=0, help="schedule timestamp for video upload")
# 	args = parser.parse_args()
#     # python3 ./uploader.py -i 'your sessionid' -p ./download/test.mp4 -t  测试上传
# 	# uploadVideo('your sessionid', './download/test.mp4', '就问你批不批', ['热门'],[])
# 	uploadVideo(args.session_id, args.path, args.title, args.tags, args.users)
