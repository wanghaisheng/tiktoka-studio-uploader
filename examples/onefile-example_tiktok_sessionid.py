from tsup.tiktok.sessionId.uploader import  uploadVideo

if __name__ == '__main__':
	# parser.add_argument("-i", "--session_id", help="Tiktok sessionid cookie", required=True)
	# parser.add_argument("-p", "--path", help="Path to video file", required=True)
	# parser.add_argument("-t", "--title", help="Title of the video", required=True)
	# parser.add_argument("--tags", nargs='*', default=[], help="List of hashtags for the video")
	# parser.add_argument("--users", nargs='*', default=[], help="List of mentioned users for the video")
	# parser.add_argument("-s", "--schedule_time", type=int, default=0, help="Schedule timestamp for video upload")
	# parser.add_argument("--url_server", type=str, default="us", choices=["us", "www"], help="Specify the prefix of url (www or us)")
    session_id=""
    # you can try save-sessionId.py under examples directory
    
# if failed, pls try manual way
# To get it log in to your TikTok account and on the page https://www.tiktok.com/ press the F12 key on your keyboard then Application > Storage > Cookies and find the value of the sessionid cookie. You should have something like this: 7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d
    schedule_time=0
    #  864000s = 10 days

    path = "my_video.mp4"
    title = "MY SUPER TITLE"
    tags = ["Funny", "Joke", "fyp"]
    users = ["amazing dear"]
    proxy = {'http': 'http://ip:port', 'https': 'https://ip:port'}    
    url_server='us'

    uploadVideo(session_id, path, title, tags, users, url_server, schedule_time)

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