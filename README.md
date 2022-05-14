
[video demo](https://youtu.be/IXaEQG1BCkw)

currently  I am working on a web and GUI app for those want to have a try, please sponsor me



This project aims to automate the upload process for YouTube Videos. Since videos can only be publicly uploaded through the YouTube Data API by using a Google Workspaces Account (not free!), I decided to figure out a headless uploader using Selenium. This approach also bypasses API restrictions (e.g. Rate Limits/Endcards can't be set through the API).There are tons of library existing  but not for me .

AS a code dummy,I do accept any advice because of my only purpose is to get things work

**if you are a selenium guy,pls check  main branch,if not just use this playwright branch.**

## rewrite it with microsoft playwright

1.speed is much  faster than selenium version

2.you dont have to worry browser driver any more 

3.more like category setting,auto publish date,subtitle upload etc are considered


## steps you can reproduce 
if anything you dont understand ,just google it first,for example  firefox profile

1. Download lastest firefox,open new tab and insert:    
```
about:profiles
```
一般来说 一个youtube帐号要新建一个profile
文件夹可以选在assets下

2.install firefox addon, **Cookie-Editor**，mannually login into youtube channel，click profile icon, choose english language,export a  cookie.json 




3. if you want to modify source code, use as a library for your project,pls do    
```

git clone https://github.com/wanghaisheng/ytb_up
pip install -r requirements.txt

all codes under **ytb_up**, twist them as you wish

```
4. if you are dumb as me, wanna a try,run demo project
```
git clone https://github.com/wanghaisheng/autovideo

conda create -n autovideo python=3.9
conda activate autovideo

pip install -r requirements.txt

python auto_video.py
```

woola  you can see a ugly gui  for your demo purpose

5. use existing without modification as a lib
```
pip install ytb-up
```


# features YOU MAY NEED

# 1. proxy support
auto detect whether need a proxy 

# 2. cookie support
for those multiple channels under same google account


pls check 
https://github.com/microsoft/playwright/issues/12616

manually change no_restriction to

>        "sameSite": "None",


# 3. schedule time publish

you can explictly specify a date and time for each video or you can set publish policy and daily public count,for example,daily count is 4,you got 5 videos,then first 4 will be published 1 day after the upload date ,the other 1 will be 2 days after the upload date
# 4. fix google account verify

# 5. seleniumwire

THANKS FOR 
1. https://github.com/ContentAutomation/YouTubeUploader
2. https://github.com/offish/opplast
3. other I CAN NOT REMEMBER


video file format: pls use mp4、webm
douyin title format:
bababala #话题1 #话题2 @好友1 @好友2

# 6 feed me hamburger

## 1hamburger is good 

![1hamburger](https://user-images.githubusercontent.com/2363295/167280864-7f8fe860-7258-4267-8e54-a8f0a4eb870b.png)


## 2hamburger  is great

![2hamburger](https://user-images.githubusercontent.com/2363295/167280866-521fbc81-8c30-4b5d-b7db-6e1c4549f2e6.png)


## 5hamburger I wont need lose weight. 

![5hamburger](https://user-images.githubusercontent.com/2363295/167280869-5e01a666-f10e-4620-b6c5-a12bfe2c25fb.png)


