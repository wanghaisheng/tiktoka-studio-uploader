from upgenius.tiktok.sessionId.uploader import  upload2TiktokSessionId
from upgenius.utils.tools import get_duration_timestamp
year_target = 2023
month_target = 8
day_target = 31
hour_target = 12
minute_target = 0
second_target = 0
schedule_time=get_duration_timestamp(year_target,month_target,day_target,hour_target,minute_target,second_target)
default_tags=["Funny", "Joke", "fyp"]
if __name__ == '__main__':
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

	if args.schedule_time is None:args.schedule_time =schedule_time
	if args.tags is None:args.tags =default_tags

	upload2TiktokSessionId(args.session_id, args.path, args.title, args.tags, args.users, args.url_server, args.schedule_time)
    # python newfile.py -i 'your sessionid' -p ./download/test.mp4 -t titlestring --tags []