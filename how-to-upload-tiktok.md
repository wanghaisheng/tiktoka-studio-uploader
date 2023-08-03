### manually find the sessionId or cookies

Log into Tiktok on any desktop web browser, then open your browser's developer tools (also known as "inspect") and look for the value of the p-b cookie in the following menus:

*    Chromium: Devtools > Application > Cookies > tiktok.com
*    Firefox: Devtools > Storage > Cookies
*    Safari: Devtools > Storage > Cookies

### automatically get cookies or sessionId

get cookies for your tiktok accounts without any efforts,for those proxy setting, adjust the code as you wish.

```
python examples/saveCookie.py
```

or
```
python examples/save-tiktok-sessionId.py
```

### for those not that tech savy

1. install python on your computer. if you do not know how ,check here

```
https://docs.python.org/3.9/using/index.html
```

3. just download zip from here

```
https://github.com/wanghaisheng/youtube-auto-upload/archive/refs/heads/playwright.zip
```

4. unzip this into anywhere you like，open terminal:

```
pip install -r requirements.txt

python setup.py install
```


5. run upload demo

just use command in console to test it 

```
python examples/onefile-example_tiktok_sessionid_command.py
```

or 

how to call this lib in your own project 

```
python examples/onefile-example_tiktok_sessionid.py
```

### for those tech guy

1. we recommend you setup 2FA for youtube channel

2. install python on your computer. if you do not know how ,check here

```
https://docs.python.org/3.9/using/index.html
```

3. download code

```

git clone https://github.com/wanghaisheng/youtube-auto-upload

pip install -r requirements.txt

python setup.py install

```

all codes under **ytb_up**, twist them as you wish

4. There is a selenium and playwright version, choose the one you like
   switch branches to find it

5. use existing without modification as a lib

```
pip install ytb-up
```
