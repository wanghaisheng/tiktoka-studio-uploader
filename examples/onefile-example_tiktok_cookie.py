cookies_list = [
    {
        'name': 'sessionid',
        'value': '**your session id**',
        'domain': 'https://tiktok.com',
        'path': '/',
        'expiry': '10/8/2023, 12:18:58 PM'
    }
]

videos = [
    {
        'video': 'video0.mp4',
        'description': 'Video 1 is about ...'
    },
    {
        'video': 'video1.mp4',
        'description': 'Video 2 is about ...'
    }
]


failed_videos = upload_videos(videos=videos, cookies_list=cookies_list)

for video in failed_videos: # each input video object which failed
    print(f'{video['video']} with description "{video['description']}" failed')


