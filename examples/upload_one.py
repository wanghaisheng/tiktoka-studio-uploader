from ytb_up import Upload


if __name__ == "__main__":
    uploadsetting = context['uploadsetting']
    profilepath =uploadsetting['firefoxprofile']
    CHANNEL_COOKIES=uploadsetting['CHANNEL_COOKIES']
    driverpath =uploadsetting['driverpath']
    prefertags=uploadsetting['prefertags']
    if post_id:
        postlist=getpostforid(context,post_id)
    else:

        postidlist, postlist = getpostforupload(context)
    if len(postlist)==0:
        print('video have not been prepared')
    else:
        today = date.today()
        # publish_date=''
        counter =0

        publish_date =datetime(today.year, today.month, today.day, 20, 15) 
        for post in postlist:
            counter =counter +1
            if counter<int(uploadsetting['dailycount']):
                publish_date += timedelta(days=9)

            else:
                publish_date += timedelta(days=9)
                publish_date += timedelta(months=int(int(i)/30), days=int(int(i)/int(setting['dailycount'])))
                        
            post_id = post['post_id']
            uploadmp4 = post['uploadmp4']
            tags =post['tags']
            post_title =post['post_title']
            title = post['title']
            rapidtags = post['rapidtags']
            des = post['des'][:4500]
            # predes = "All the posts in this video are jokes and for comedic purposes only.\nFunny memes daily, Subscribe for best memes compilation & reddit clean memes 2021"
            prefertags=uploadsetting['prefertags']
            thumbpath = post['thumbpath']
            posfnsfw=post['postnsfw']
            # des = predes
            # formattitle = post_title+"|aww daily memes"
            # if prefertags and not prefertags=='':
            #         prefertags =prefertags+rapidtags
            # tags =prefertags+tags
            # print(os.getcwd()+os.sep+uploadmp4)
            # print(tags)
            # print(os.getcwd()+os.sep+ thumbpath)
            formattitle = post_title+"| The Millionaire Fastlane"
            if len(post_title) > 100:
                formattitle = post_title[:80]+"| The Millionaire Fastlane"
            uploadmp4= os.getcwd()+os.sep+uploadmp4

            title=formattitle
            if os.path.exists(uploadmp4) and os.path.getsize(uploadmp4):
                print('start upload video',post_id,title)
                description =des[:4800]

                thumbnail= os.getcwd()+os.sep+ thumbpath
                tags=[tags[:400]]

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
                        profilepath,
                        CHANNEL_COOKIES=CHANNEL_COOKIES,
                        headless=True,
                        executable_path =driverpath
                    )
                else:
                    print('we need for proxy ')

                    upload = Upload(
                        # use r"" for paths, this will not give formatting errors e.g. "\n"
                        profilepath,
                        proxy_option=options,
                        headless=True,
                        executable_path =driverpath,
                        CHANNEL_COOKIES=CHANNEL_COOKIES
                    )
                if not posfnsfw:

                    # publish_date = datetime.strptime(publish_date, "%Y-%m-%d %H:%M:%S")               
                    print("-----------",uploadsetting['publishpolicy'],type(uploadsetting['publishpolicy']))
                    was_uploaded =False
                    if uploadsetting['publishpolicy']=="0" or uploadsetting['publishpolicy']=="1":
                        was_uploaded, upload_video_id = upload.upload(
                            uploadmp4,
                            title=title[:99],
                            description=des,
                            thumbnail=thumbnail,
                            tags=rapidtags,
                            publishpolicy=uploadsetting['publishpolicy']
                        )
                    else:

                        was_uploaded, upload_video_id = upload.upload(
                            uploadmp4,
                            title=title[:99],
                            description=des,
                            thumbnail=thumbnail,
                            tags=rapidtags,
                            publishpolicy="2",
                            publish_date=publish_date
                        )

                    # was_uploaded, video_id = upload.upload(uploadmp4,title,description,thumbnail,tags,CHANNEL_COOKIES)
                    print("upload status",was_uploaded)
                    if was_uploaded:
                        print(f"{post_id} has been uploaded to YouTube")

                        updatescrapemetakv(context,post_id,'status',1)

                        print(f"{post_id} status 0 to 1")
                        upload.close()

                else:
                    print('this is a nsfw post',posfnsfw,'--\n',post_id)
            else:
                print('upload video is broken or missing',uploadmp4)

