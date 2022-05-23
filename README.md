<!-- MANPAGE: BEGIN EXCLUDED SECTION -->
<div align="center">

[![YTB-UP](https://raw.githubusercontent.com/wanghaisheng/youtube-auto-upload/master/assets/images.png)](#readme)

[![Release version](https://img.shields.io/github/v/release/wanghaisheng/youtube-auto-upload?color=brightgreen&label=Download&style=for-the-badge)](#release-files "Release")
[![PyPi](https://img.shields.io/badge/-PyPi-blue.svg?logo=pypi&labelColor=555555&style=for-the-badge)](https://pypi.org/project/ytb-up "PyPi")
[![Donate](https://img.shields.io/badge/_-Donate-red.svg?logo=githubsponsors&labelColor=555555&style=for-the-badge)](https://github.com/sponsors/wanghaisheng "Donate")
[![Sponsors](https://img.shields.io/github/sponsors/wanghaisheng)]("Sponsors")
<!-- [![Discord](https://img.shields.io/discord/807245652072857610?color=blue&labelColor=555555&label=&logo=discord&style=for-the-badge)](https://discord.gg/xxxxx "Discord") -->
[![Supported Sites](https://img.shields.io/badge/-Supported_Sites-brightgreen.svg?style=for-the-badge)](supportedsites.md "Supported Sites")
[![License: Unlicense](https://img.shields.io/badge/-Unlicense-blue.svg?style=for-the-badge)](LICENSE "License")
[![Commits](https://img.shields.io/github/commit-activity/m/wanghaisheng/youtube-auto-upload?label=commits&style=for-the-badge)](https://github.com/wanghaisheng/youtube-auto-upload/commits "Commit History")
[![Last Commit](https://img.shields.io/github/last-commit/wanghaisheng/youtube-auto-upload/playwright?label=&style=for-the-badge)](https://github.com/wanghaisheng/youtube-auto-upload/commits "Commit History")

</div>
<!-- MANPAGE: END EXCLUDED SECTION -->



**I  have released one draft version GUI to ease the usage for those non-coding people that want a one click easy solution.  It's been tested by about 5 friends. You can check it. If you sponsor me you can get the exe version on Windows**

[Get the early bird version. Please sponsor me here](https://github.com/sponsors/wanghaisheng)

or click any link you find in the repo

![Tiktoka Uploader](https://user-images.githubusercontent.com/2363295/168556947-a1c3025a-aa76-4873-9d7f-d4475712296a.png)

![Tiktoka Uploader GUI](https://raw.githubusercontent.com/wanghaisheng/youtube-auto-upload/master/assets/autovideopublisher_cCU22EfevT.png)


A cross platform GUI is being developed.

In the future I plan to add more features like invisible watermark to protect your copyright from theft and cross platform publish that you may post videos not only on Youtube.


## video demo 

[English version detailed intro and demo ](https://youtu.be/Xh-Dmm1POBo)

https://youtu.be/tp69CzU1y7s

https://youtu.be/IXaEQG1BCkw

https://youtu.be/Sqj0uO9VCy4


------

## features included in the GUI version

### no limit of video counts 

1000+ is easy especially for backup usage as private 

###  you dont have to edit all metadata one by one
description combine from prefix,suffix and video filename
tags combine from preferred tags and ai based generated topic related tags
pulish time can automatically set without any effort

### auto generate thumbnail from video hightlight

you can using these as startpoint to add overlay text to make it more clickbait to get traffic

### auto add Free copyright music 

some music is the secret weapon to traffic, you need dig it by yourself.and also not to share with others

### invisible watermark

at some day if you got viral  someone will steal your content to repost over other platform, cut off your logo or other visible watermark,with this invisible/hidden watermark technology, you can hardless lost the battle

### multi account and multi channel under one account

as newbie you will not want to have egg stay in one blanket.it will save your time to success

### auto set schedule time to public for each video
bulk publish .
it seems no other lib support this feature yet

### video upload in batch

all you need is choose the video dir


### Installed on PC, access from PC and mobile 


------

This project aims to automate the upload process for YouTube Videos. Since videos can only be publicly uploaded through the YouTube Data API by using a Google Workspaces Account (not free!), I decided to figure out a headless uploader using Selenium. This approach also bypasses API restrictions (e.g. Rate Limits/Endcards can't be set through the API).There are tons of library existing  but not for me .

AS a code dummy,I do accept any advice because of my only purpose is to get things work

**if you are a selenium guy,pls check  main branch,if not just use this playwright branch.**

## rewrite it with microsoft playwright

1.speed is much  faster than selenium version

2.you dont have to worry browser driver any more 

3.more like category setting,auto publish date,subtitle upload etc are considered


## USAGE
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

git clone https://github.com/wanghaisheng/youtube-auto-upload

pip install -r requirements.txt

python onefile-example.py 

all codes under **ytb_up**, twist them as you wish

```

4. we got selenium and playwright two version ,choose as you like
switch branch you can find that 

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

auto verify is not working,you need manually input verify code in the browser


# 5. 

THANKS FOR 
1. https://github.com/ContentAutomation/YouTubeUploader
2. https://github.com/offish/opplast
3. other I CAN NOT REMEMBER



# 6 feed me hamburger


# 7. Join Online video chat and easily share your desktop for debug your issue

https://vdo.ninja/?room=Youtube_Auto_Upload&broadcast


