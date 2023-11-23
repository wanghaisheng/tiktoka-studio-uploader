**Update 2023-11-23**

1. change  debug  to log_level, add logger field if you want to wrap this lib in your code,you can pass your own logger here to control output format.

2. add use_undetected_playwright ,try to avoid insecure browser detection 

3. update log util to better reading

4. update insecure browser detect

5. update examples 

6. add placeholder for alternate video meta such as title,description,srt file 




**Update 2023-11-22**

1. add selenium support  for tiktok 

python examples/onefile-example_tiktok_selenium_adspower.py

python examples/onefile-example_tiktok_selenium.py

2. fix other issues




**Update 2023-09-17**

1. add batch file process for tiktok 

python examples/batch_files_in_excel_tiktok.py

python examples/batch_files_in_json_youtube.py

2. fix other issues


**Update 2023-08-30**

1. add undetected-playwright support to use as embed anti-detect browser

2. add very its you and insecure browser detection during sigin in

3. add youtube models for later gui development

4. change previous camel variable in youtube upload to underscore

5. fix other issues


**Update 2023-08-25**
1. we add all in one bash script for newbee to have a try.
for tiktok
>test-tiktok-manual-sessionId.sh
for youtube
>test-youtube-windows.sh

1. add test-youtube-windows.sh to help tiktokers 

2. add test-tiktok-manual-sessionId.sh to help youtubers 

3. examples\save-tiktok-sessionId.py to auto export sessionid

4. examples\save-youtube-Cookie.py to auto export youtube cookie files




**Update 2023-08-03**

1. we now support tiktok now by sessionId way,and you can even grab a sessionid in your local pc and use it in your remote server.check [tiktok how to doc](./how-to-upload-tiktok.md)

2. Hungup the  support an embed fake browser fingerprint to tiktok 

3. will support tiktok official api 

for tiktok part,lately there is official api coming, I created another repo for building with official api way:

https://github.com/wanghaisheng/tiktok-opensdk-web


4. will support playwright way for tiktok, especially for the rotate capcha verify


