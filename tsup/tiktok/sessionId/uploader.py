import requests
import json
import time
import datetime
from urllib.parse import urlencode
from tsup.tiktok.sessionId.x_bogus_ import get_x_bogus
from tsup.tiktok.sessionId.util import assertSuccess, printError, getTagsExtra, uploadToTikTok, log, getCreationId
import urllib3
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


def upload2TiktokSessionId(session_id, video, title, tags, users=[], url_prefix="us", schedule_time: int = 0, proxy: dict = None):
	tiktok_min_margin_schedule_time =  900  # 15 minutes
	tiktok_max_margin_schedule_time = 864000  # 10 days
	margin_to_upload_video = 300  # 5 minutes

	min_schedule_time = datetime.datetime.utcnow().timestamp() + tiktok_min_margin_schedule_time + margin_to_upload_video
	max_schedule_time = datetime.datetime.utcnow().timestamp() + tiktok_max_margin_schedule_time

	if schedule_time == 0:
		pass
	elif schedule_time < min_schedule_time:
		print(f"[-] Can not schedule video in less than {(tiktok_min_margin_schedule_time + margin_to_upload_video) // 60} minutes")
		return False
	elif schedule_time > max_schedule_time:
		print(f"[-] Can not schedule video in more than {tiktok_max_margin_schedule_time // 86400} days")
		return False


	session = requests.Session()

	if proxy:
		session.proxies.update(proxy)
	session.cookies.set("sessionid", session_id, domain=".tiktok.com")
	session.verify = True
	print(f'session proxy:{session.proxies}')
	headers = {
		'User-Agent': UA
	}
	url = f"https://{url_prefix}.tiktok.com/upload/"
	r = session.get(url, headers=headers)
	if not assertSuccess(url, r):
		return False
	creationid = getCreationId()
	url = f"https://{url_prefix}.tiktok.com/api/v1/web/project/create/?creation_id={creationid}&type=1&aid=1988"
	headers = {
		"X-Secsdk-Csrf-Request": "1",
		"X-Secsdk-Csrf-Version": "1.2.8"
	}
	r = session.post(url, headers=headers)
	if not assertSuccess(url, r):
		return False
	try:
		tempInfo = r.json()['project']
	except KeyError:
		print(f"[-] An error occured while reaching {url}")
		print("[-] Please try to change the --url_server argument to the adapted prefix for your account")
		return False
	creationID = tempInfo["creationID"]
	projectID = tempInfo["project_id"]
	# 获取账号信息
	url = f"https://{url_prefix}.tiktok.com/passport/web/account/info/"
	r = session.get(url)
	if not assertSuccess(url, r):
		return False
	# user_id = r.json()["data"]["user_id_str"]
	log("Start uploading video")
	video_id = uploadToTikTok(video, session)
	if not video_id:
		log("Video upload failed")
		return False
	log("Video uploaded successfully")
	time.sleep(2)
	result = getTagsExtra(title, tags, users, session, url_prefix)
	time.sleep(3)
	title = result[0]
	text_extra = result[1]
	postQuery = {
		'app_name': 'tiktok_web',
		'channel': 'tiktok_web',
		'device_platform': 'web',
		'aid': 1988
	}
	data = {
		"upload_param": {
			"video_param": {
				"text": title,
				"text_extra": text_extra,
				"poster_delay": 0
			},
			"visibility_type": 0,
			"allow_comment": 1,
			"allow_duet": 0,
			"allow_stitch": 0,
			"sound_exemption": 0,
			"geofencing_regions": [],
			"creation_id": creationID,
			"is_uploaded_in_batch": False,
			"is_enable_playlist": False,
			"is_added_to_playlist": False
		},
		"project_id": projectID,
		"draft": "",
		"single_upload_param": [],
		"video_id": video_id,
		"creation_id": creationID
	}
	if schedule_time == 0:
		pass
	elif schedule_time > min_schedule_time:
		# Confirm again because the video upload can be very long
		data["upload_param"]["schedule_time"] = schedule_time
	else:
		log(f"Video schedule time is less than {tiktok_min_margin_schedule_time // 60} minutes in the future, the upload process took more than"
			f"the {margin_to_upload_video // 60} minutes of margin to upload the video")
		return False
	postQuery['X-Bogus'] = get_x_bogus(urlencode(postQuery), json.dumps(data, separators=(',', ':')), UA)
	url = f'https://{url_prefix}.tiktok.com/api/v1/web/project/post/'
	headers = {
		'Host': f'{url_prefix}.tiktok.com',
		'content-type': 'application/json',
		'user-agent': UA,
		'origin': 'https://www.tiktok.com',
		'referer': 'https://www.tiktok.com/'
	}
	r = session.post(url, params=postQuery, data=json.dumps(data, separators=(',', ':')), headers=headers)
	if not assertSuccess(url, r):
		log("Publish failed")
		printError(url, r)
		return False
	if r.json()["status_code"] == 0:
		log(f"Published successfully {'| Scheduled for ' + str(schedule_time) if schedule_time else ''}")
	else:
		log("Publish failed")
		printError(url, r)
		return False

	return True


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--session_id", help="Tiktok sessionid cookie", required=True)
	parser.add_argument("-p", "--path", help="Path to video file", required=True)
	parser.add_argument("-t", "--title", help="Title of the video", required=True)
	parser.add_argument("--tags", nargs='*', default=[], help="List of hashtags for the video")
	parser.add_argument("--users", nargs='*', default=[], help="List of mentioned users for the video")
	parser.add_argument("-s", "--schedule_time", type=int, default=0, help="Schedule timestamp for video upload")
	parser.add_argument("--url_server", type=str, default="us", choices=["us", "www"], help="Specify the prefix of url (www or us)")
	args = parser.parse_args()
	# python3 ./uploader.py -i 'your sessionid' -p ./download/test.mp4 -t  测试上传
	# uploadVideo('your sessionid', './download/test.mp4', '就问你批不批', ['热门'],[])
	uploadVideo(args.session_id, args.path, args.title, args.tags, args.users, args.url_server, args.schedule_time)
