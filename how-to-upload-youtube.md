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

4. get cookies for your youtube channel without any efforts,for those proxy setting, adjust the code as you wish.
   If given user's account have only onedefault video channel. Many users (myself included) manage multiple channels under the same youtube account,so after login in, you need switch to the channel you want video uploading to save different cookie.json for each channel. then you can close the openning browser.

```
python examples/saveCookie.py
```

5. run upload demo

```
python examples/onefile-example_youtube.py
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
