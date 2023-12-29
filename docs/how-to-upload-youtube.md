you can run 

>bash test-youtube-windows.sh


### for those not that tech savy

1. install python on your computer. if you do not know how ,check here

```
https://docs.python.org/3.9/using/index.html
```

3. just download zip from here

```
https://github.com/wanghaisheng/tiktoka-studio-uploader/archive/refs/heads/playwright.zip
```

4. unzip this into anywhere you like，open terminal,type:
```
bash test-youtube-windows.sh
```

if you dig this bash script, you can find it run the following:

```
pip install -r requirements.txt

python setup.py install
```

4.1. get cookies for your youtube channel without any efforts,for those proxy setting, adjust the code as you wish.
   If given user's account have only onedefault video channel. Many users (myself included) manage multiple channels under the same youtube account,so after login in, you need switch to the channel you want video uploading to save different cookie.json for each channel. then you can close the openning browser.

```
python examples/save-youtube-Cookie.py
```

4.2. run upload demo for different operation systems as you like.

```
python examples/onefile-example_youtube.py
python examples/onefile-example_youtube-windows.py
python examples/onefile-example_youtube-mac.py

```

### for those tech guy

1. we recommend you setup 2FA for youtube channel

2. install python on your computer. if you do not know how ,check here

```
https://docs.python.org/3.9/using/index.html
```

3. download code

```

git clone https://github.com/wanghaisheng/tiktoka-studio-uploader


```

## macos


```

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python setup.py install
```

## windows

```
python -m venv .venv

source .venv/Scripts/activate
pip install -r requirements.txt

python setup.py install
```



all codes under **ytb_up**, twist them as you wish

4. There is a selenium and playwright version, choose the one you like
   switch branches to find it

5. use existing without modification as a lib

```
pip install upgenius
```
