"""setup script for installing python dependencies in youtube-auto-upload toolkit"""


import subprocess
import time
from upgenius.utils.webdriver.setupPL import checkRequirments


def getCookie(
    browserType: str = "firefox",
    proxyserver: str = "",
    channelname: str = "youtube-channel",
    url: str = "www.youtube.com",
):
    if browserType in ["firefox", "webkit", ""]:
        if proxyserver:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                # + ' --device "iPad Pro 11 landscape" '
                + " --proxy-server "
                + proxyserver
                + " --lang 'en-GB' --save-storage="
                + channelname
                + "-cookie.json "
                + url
            )
        else:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                + " --lang 'en-GB' --save-storage="
                + channelname
                + "-cookie.json "
                + url
            )
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        print(result)
        if result.returncode:
            print(f"failed to save cookie file:{result.stderr}")
        else:
            print("just check your cookie file", channelname + "-cookie.json")


def loadCookie(
    browserType: str = "firefox",
    proxyserver: str = "",
    cookiefile: str = "cookie json file",
    url: str = "www.youtube.com",
):
    if browserType in ["firefox", "webkit", ""]:
        if proxyserver:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                # + ' --device "iPad Pro 11 landscape" '
                + " --proxy-server "
                + proxyserver
                + " --lang 'en-GB' --load-storage="
                + cookiefile
                + " "
                + url
            )
        else:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                + " --lang 'en-GB' --load-storage="
                + cookiefile
                + " "
                + url
            )
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        print(result)
        if result.returncode:
            print(f"failed to load cookie file:{result.stderr}")
        else:
            print("just check your cookie file", cookiefile )






if __name__ == "__main__":
    # checkRequirments("firefox")
    # checkRequirments("webkit")
    # checkRequirments("chromium")
    checkRequirments()
    sites = [
        "https://www.youtube.com/upload?persist_gl=1",
        "https://www.tiktok.com",
        "https://www.douyin.com",
        "https://www.tiktok.com/login/phone-or-email/email",
    ]
# channelname is your account name or something else
# for youtube
loadCookie(browserType='firefox',proxyserver='socks5://127.0.0.1:1080',cookiefile='fastlane-cookie.json',url=sites[0])

# for tiktok
# i7SNiSG8V7jND^
# offloaddogsboner@outlook.com
# getCookie(
#     browserType="firefox",
#     proxyserver="socks5://127.0.0.1:1080",
#     channelname="offloaddogsboner",
#     url=sites[3],
# )
# unboxdoctor@outlook.com
# 95Qa*G*za5Gb
# getCookie(
#     browserType="firefox",
#     proxyserver="socks5://127.0.0.1:1080",
#     channelname="",
#     url=sites[0],
# )


# for douyin
# getCookie(browserType='firefox',proxyserver='socks5://127.0.0.1:1080',channelname='',url=sites[2])
