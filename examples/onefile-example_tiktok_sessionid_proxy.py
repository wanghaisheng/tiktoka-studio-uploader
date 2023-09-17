from tsup.tiktok.sessionId.uploader import  upload2TiktokSessionId
from tsup.utils.tools import get_duration_timestamp
def videoMetaString_timestamp():
    # targetDateTime in following format:timestamp  ,you need calculate by yourself
    schedule_time=0
    #
    #  864000s = 10 days


    session_id=""
    # you can try save-sessionId.py under examples directory
# if failed, pls try manual way
# To get it log in to your TikTok account and on the page https://www.tiktok.com/ press the F12 key on your keyboard then Application > Storage > Cookies and find the value of the sessionid cookie. You should have something like this: 7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d


    path = "my_video.mp4"
    title = "MY SUPER TITLE"
    tags = ["Funny", "Joke", "fyp"]
    users = ["amazing dear"]
    proxy = {'http': 'http://ip:port', 'https': 'https://ip:port'}    
    url_server='us'
    isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)
    if isupload==False:
        
        url_server='www'
        isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)    
def videoMetaString():

        
    # targetDateTime in following format

    year_target = 2023
    month_target = 8
    day_target = 31
    hour_target = 12
    minute_target = 0
    second_target = 0

    schedule_time=get_duration_timestamp(year_target,month_target,day_target,hour_target,minute_target,second_target)
# Note that you cannot schedule a video more than 10 days in advance.


    session_id="5139870b7334ad6b92e7e8ca2a3ce2ca"
    # you can try save-sessionId.py under examples directory
# if failed, pls try manual way
# To get it log in to your TikTok account and on the page https://www.tiktok.com/ press the F12 key on your keyboard then Application > Storage > Cookies and find the value of the sessionid cookie. You should have something like this: 7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d


    path = "tests/1.mp4"
    title = "MY SUPER TITLE"
    tags = ["Funny", "Joke", "fyp"]
    users = ["amazing dear"]
    proxy = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}    
    url_server='us'
    
    print(f'start to upload video:{path} to tiktok')
    
    isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time,proxy)
    if isupload==False:
        
        url_server='www'
        isupload=upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time,proxy)
        
    
def videoMetaJson():
    # readjsonfile
    year_target = 2023
    month_target = 8
    day_target = 31
    hour_target = 12
    minute_target = 0
    second_target = 0
    session_id=""
    # you can try save-tiktok-sessionId.py under examples directory
    
# if failed, pls try manual way
# To get it log in to your TikTok account and on the page https://www.tiktok.com/ press the F12 key on your keyboard then Application > Storage > Cookies and find the value of the sessionid cookie. You should have something like this: 7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d
    schedule_time=0
    #target date and time
    #
    #  864000s = 10 days

    path = "my_video.mp4"
    title = "MY SUPER TITLE"
    tags = ["Funny", "Joke", "fyp"]
    users = ["amazing dear"]
    proxy = {'http': 'http://ip:port', 'https': 'https://ip:port'}    
    url_server='us'

    upload2TiktokSessionId(session_id, path, title, tags, users, url_server, schedule_time)


if __name__ == '__main__':
	# parser.add_argument("-i", "--session_id", help="Tiktok sessionid cookie", required=True)
	# parser.add_argument("-p", "--path", help="Path to video file", required=True)
	# parser.add_argument("-t", "--title", help="Title of the video", required=True)
	# parser.add_argument("--tags", nargs='*', default=[], help="List of hashtags for the video")
	# parser.add_argument("--users", nargs='*', default=[], help="List of mentioned users for the video")
	# parser.add_argument("-s", "--schedule_time", type=int, default=0, help="Schedule timestamp for video upload")
	# parser.add_argument("--url_server", type=str, default="us", choices=["us", "www"], help="Specify the prefix of url (www or us)")


# videos = [
#     {
#         "path": "upload.mp4",
#         "description": "This is the first upload"
#     },
#     {
#         "filename": "upload.mp4",
#         "desc": "This is my description"
#     }
# ]
    videoMetaString()