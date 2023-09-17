from tsup.tiktok.sessionId.get_sessionid import  ExtractSessionid

if __name__ == '__main__':
    proxy={
            'http' : "socks5://127.0.0.1:1080",
            'https' : "socks5://127.0.0.1:1080"
        }
    # if not use proxy, comment out the next line
    #proxy=None
    E = ExtractSessionid(proxy=proxy)
# console
#     E.choice()
# 
    username="offloaddogsboner@outlook.com"
    password="i7SNiSG8V7jND^"
    E.ExtractSessionidSingle(username,password)

# if failed, pls try manual way
# To get it log in to your TikTok account and on the page https://www.tiktok.com/ 
# press the F12 key on your keyboard then Application > Storage > Cookies and 
# find the value of the sessionid cookie. You should have something 
# like this: 7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d