there is a GUI demo you can just use that

https://github.com/wanghaisheng/autovideo

This project aims to automate the upload process for YouTube Videos. Since videos can only be publicly uploaded through the YouTube Data API by using a Google Workspaces Account (not free!), I decided to figure out a headless uploader using Selenium. This approach also bypasses API restrictions (e.g. Rate Limits/Endcards can't be set through the API).There are tons of library existing  but not for me .

AS a code dummy,I do accept any advice because of my only purpose is to get things work


**if you encounter any issue,pls change headless to false,watch what happens in your browser,you will find the clue to your issue.Take care of title,description,tags word/character limit youtube **

# setup 

1. Download lastest firefox,open new tab and insert:    
```
about:profiles
```

usually  you need prepare/create a new profile for a youtube channel. profile file path can be under **assets**
一般来说 一个youtube帐号要新建一个profile
文件夹可以选在assets下

2.install firefox addon, **Cookie-Editor**，mannually login into youtube channel，click profile icon, choose english language,export a  cookie.json 


3. if you want to ajust source code, pls do    
```

git clone https://github.com/wanghaisheng/ytb_up
pip install -r requirements.txt

all codes under **ytb_up**, twist them as you wish

```
4. run demo project
```
git clone https://github.com/wanghaisheng/autovideo

conda create -n autovideo python=3.9
conda activate autovideo

下面这两个二选一就行
pip install -i http://mirrors.aliyun.com/pypi/simple/ requests pillow itemdbs selenium-wire moviepy ytb_up

pip install -i  https://pypi.tuna.tsinghua.edu.cn/simple requests pillow itemdbs selenium-wire moviepy ytb_up
python auto_video.py
```
5. use as a lib
```
pip install ytb-up
```

6. publishpolicy setting


配置文件说明 
publishpolicy：1 表示上传以后立即公开  0 表示上传以后保持私享 2表示结合每天发布数量和视频文件夹中的数量 从上传当日起开始定时公开    
publishpolicy：1 pulibc   0 private 2 schedule publish 表示结合每天发布数量和视频文件夹中的数量 从上传当日起开始定时公开



# features YOU MAY NEED

# 1. proxy support
auto detect whether need a proxy 

# 2. cookie support
for those multiple channels under same google account

# 3. schedule time publish

you can explictly specify a date and time for each video or you can set publish policy and daily public count,for example,daily count is 4,you got 5 videos,then first 4 will be published 1 day after the upload date ,the other 1 will be 2 days after the upload date
# 4. fix google account verify

# 5. seleniumwire

THANKS FOR 
1. https://github.com/ContentAutomation/YouTubeUploader
2. https://github.com/offish/opplast
3. other I CAN NOT REMEMBER


# buy me a coffee

https://www.buymeacoffee.com/madegamedev


# future plan

1. playwright support
2. 
