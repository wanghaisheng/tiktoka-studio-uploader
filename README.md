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


just launched on product hunt 

<a href="https://www.producthunt.com/posts/tiktoka-studio?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-tiktoka&#0045;studio" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=347723&theme=light" alt="Tiktoka&#0032;Studio - one&#0032;in&#0032;all&#0032;toolbox&#0032;for&#0032;social&#0032;media&#0032;video&#0032;publish | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>


**I  have released one draft version of a GUI version to make the usage for those non-coding people that want a one click easy solution.  It's been tested by about 5 friends. You can check it out if you sponsor me. You can get the exe version on Windows**

please DM me at tiktokadownloader@gmail.com after sponsor, I have not find a proper way to automatically to send the package yet



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

* → no limit of video counts

you may got hundreds of historical videos or prepare 200+ video for new product.

1000+ is possible especially for archive or backup usage as private

**does this uploader (gui version specifically) bypass the youtube upload limit of 100 uploads per day? could it do 10k uploads in a day?**

No.be aware of that this is automation instead of crack thing.If it can be done,definitely would be flagged as spam and you lost your account ,that is not the price you want to pay
all of automation task are meant to act like human but ease your boring hand work

![image](https://user-images.githubusercontent.com/2363295/170889182-e3a12d5f-d1cb-45db-93a0-2ce8e405c9d1.png)


* → you don't have to edit all metadata one by one

Full description combine from prefix, suffix and video filename tags combine from preferred tags and AI based generated topic related tags publish time can automatically set without any effort

* → auto generate thumbnail from video highlight

you can using these as starting point to add overlay text to make it more click-bait to get traffic

* → auto generate Tags from AI
It can detect keywords search and  existing video gaps in your niche and generate suggestions. 

* → auto add Free copyright music
some music is the secret weapon to traffic, you need dig it by yourself.and also not to share with others
* → invisible watermark
at some day if you got viral someone will steal your content to re-post over other platform, cut off your logo or other visible watermark,with this invisible/hidden watermark technology, you can hardly lost the battle
* → multi-account and multi-channel under one account
as a newbie you will not want to be limited to only using one account. It will save your time to success
* → auto set schedule time to public for each video
bulk publish. it seems no other lib supports this feature yet
you can explicitly specify a date and time for each video or you can set publish policy and daily public count, for example, daily count is 4, you got 5 videos, then first 4 will be published 1 day after the upload date, the other 1 will be 2 days after the upload date

* → video upload in batch
for those who want a one click setting and went to bed ,get jobs all  done after wake up in th morning
all you need is choose the video directory
* → Installed on PC, access from PC and mobile

We'd love to hear your feedback on our new feature! 😊



------

This project aims to automate the upload process for YouTube Videos. Since videos can only be publicly uploaded through the YouTube Data API by using a Google Workspaces Account (not free!), I decided to figure out a headless uploader using Selenium and Playwright. This approach also bypasses API restrictions (e.g. Rate Limits/Endcards can't be set through the API).There are tons of library existing  but not for me .

AS a code dummy, I do accept any advice because my only purpose is to get things working

**if you are a selenium guy, pls check  main branch, if not just use this playwright branch.**

## rewrite it with microsoft playwright

1. speed is much  faster than selenium version

2. you don't have to worry about browser driver any more 

3. more like category setting, auto publish date, subtitle upload etc are considered


## USAGE
if there's anything you don't understand, just google it first, for example firefox profile

1. Download the lastest Firefox, open a new tab and insert:    
```
about:profiles
```
一般来说 一个youtube帐号要新建一个profile
文件夹可以选在assets下

2.install the Firefox addon, **Cookie-Editor**，mannually login into your Youtube channel，click the profile icon, choose English language, export and save as cookie.json 



3. if you want to modify source code, use as a library for your project, pls do    
```

git clone https://github.com/wanghaisheng/youtube-auto-upload

pip install -r requirements.txt

python onefile-example.py 

all codes under **ytb_up**, twist them as you wish

```

4. There is a selenium and playwright version, choose the one you like
switch branches to find it

5. use existing without modification as a lib
```
pip install ytb-up
```

6. to get started edit onefile-example.py and enter in your CHANNEL_COOKIES path, videopath etc. Then run the file.

# features YOU MAY NEED

# 1. proxy support
auto detect whether need a proxy 

# 2. cookie support
for those with multiple channels under the one Google account


pls check 
https://github.com/microsoft/playwright/issues/12616

manually change all occurances of no_restriction in your cookies.json file to

>        "sameSite": "None",


# 3. schedule time publish

you can explictly specify a date and time for each video or you can set publish policy and daily public count, for example, daily count is 4, you got 5 videos, then first 4 will be published 1 day after the upload date, the other 1 will be 2 days after the upload date

# 4. fix Google account verify

if auto verify is not working, you need to manually input verification code into your browser


# 5. 

THANKS TO
1. https://github.com/ContentAutomation/YouTubeUploader
2. https://github.com/offish/opplast
3. other I CAN NOT REMEMBER



# 6 feed me hamburger


# 7. Join Online video chat and easily share your desktop for debugging your issues with me

https://vdo.ninja/?room=Youtube_Auto_Upload&broadcast


https://api.ossinsight.io/share/6c3c07e5-1957-4ecb-b0eb-30799badfd1b


