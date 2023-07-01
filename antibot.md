google detect security issue
tiktok has rotation capcha

# bypass slide from fakeuser browser as plan A

so capcha wont appear

## stealth.min.js

https://github.com/berstend/puppeteer-extra/blob/39248f1f5deeb21b1e7eb6ae07b8ef73f1231ab9/packages/extract-stealth-evasions/readme.md?plain=1#L13

#### Using the CDN version

You can also fetch the latest version from [gitCDN](https://gitcdn.xyz/repo/berstend/puppeteer-extra/stealth-js/stealth.min.js). For example, paste this one-liner in your browser devtools console:

```js
document.body.appendChild(
  Object.assign(document.createElement("script"), {
    src: "https://gitcdn.xyz/repo/berstend/puppeteer-extra/stealth-js/stealth.min.js",
  })
);
```

## wrapper based stealth.min.js

这个里面处理了使用代理后系统时间与代理所在位置的时区保持一致
https://github.com/Stackz7/DiscordTokenGenerator/blob/main/main.py
https://github.com/Vinyzu/Botright

https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth
https://github.com/QIN2DIM/undetected-playwright/tree/main
https://github.com/AtuboDad/playwright_stealth/issues

## other fake method

> 这个用的和 stealth js 不是一套 js，需要根据 bot 检验网站看看区别在哪里，
> https://github.com/vvanglro/cf-clearance/tree/main

## manually

https://github.com/Boris-code/feapder/blob/ba0165db2c45cb231815ccaa6e4e932905912603/docs/source_code/%E6%B5%8F%E8%A7%88%E5%99%A8%E6%B8%B2%E6%9F%93-Playwright.md?plain=1#L38

# deal capcha whenever it appear as plan B

cal rotation angle

cal drage distance

# detect fingerprint of browser

https://github.com/berstend/puppeteer-extra/issues/254
[Idea] List of detection tests in docs #254

    Distill Networks http://promos.rtm.com
    Sannysoft https://bot.sannysoft.com
    SocialNetDefender http://anonymity.space/hellobot.php
    Are You Headless? https://arh.antoinevastel.com/bots/areyouheadless
    Fingerprint2 https://fingerprintjs.com/demo
    Datadome https://datadome.co
    Recaptcha3 https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html
    Recaptcha https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php
    BrowserLeaks https://browserleaks.com/webgl
    PixelScan https://pixelscan.net

### Fingerprint test pages

These websites may be useful to test fingerprinting techniques against a web scraping software

| Test page                                                                     | Notes                                                                                                                                                                            |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| https://bot.incolumitas.com/                                                  | Very helpful and useful collection of tests                                                                                                                                      |
| https://plaperdr.github.io/morellian-canvas/Prototype/webpage/picassauth.html | canvas fingerprinting on steroids                                                                                                                                                |
| https://pixelscan.net/                                                        | Not 100% realiable as it often displays "inconsistent" to Chrome after a new update, but worth checking as the author adds new interesting detection features every now and then |
| https://browserleaks.com/                                                     | Doesn't need introduction 😉                                                                                                                                                     |
| https://f.vision/                                                             | Good quality test page from some 🇷🇺 guys                                                                                                                                         |
| https://www.ipqualityscore.com/ip-reputation-check                            | Commercial service with free reputation check against popular blacklists                                                                                                         |
| https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html      | ReCaptcha score as well as some interesting notes on how to optimize captcha solving costs                                                                                       |
| https://ja3er.com/                                                            | SSL/TLS fingerprint                                                                                                                                                              |
| https://fingerprintjs.com/demo/                                               | Good for basic tests - from people who believe and claim can create unique fingerprints "99.5%" of the time                                                                      |
| https://coveryourtracks.eff.org/                                              | -                                                                                                                                                                                |
| https://www.deviceinfo.me/                                                    | -                                                                                                                                                                                |
| https://amiunique.org/                                                        | -                                                                                                                                                                                |
| http://uniquemachine.org/                                                     | -                                                                                                                                                                                |
| http://dnscookie.com/                                                         | -                                                                                                                                                                                |
| https://whatleaks.com/                                                        | -                                                                                                                                                                                |
| https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html      | Check your reCaptcha score                                                                                                                                                       |
| https://antoinevastel.com/bots/                                               | -                                                                                                                                                                                |
| https://antoinevastel.com/bots/datadome                                       | -                                                                                                                                                                                |
| https://iphey.com/                                                            | -                                                                                                                                                                                |
| https://bot.sannysoft.com/                                                    | -                                                                                                                                                                                |
| https://webbrowsertools.com/canvas-fingerprint/                               | -                                                                                                                                                                                |
| https://webbrowsertools.com/webgl-fingerprint/                                | -                                                                                                                                                                                |
| https://fingerprint.com/products/bot-detection/                               | -                                                                                                                                                                                |
| https://abrahamjuliot.github.io/creepjs/                                      | Really creepy, the strongest of all                                                                                                                                              |

Any others people know of would be awesome!
Submitted

    F5 Network https://ib.bri.co.id/ib-bri (tenkuken)
    WhiteOps https://smitop.com/post/whiteops-data (evading-bot-detection)

notes

使用 PlaywrightAsyncDriver，也就是在 page 和 context 中都使用 add_init_script stealth.min.js 的方式， 在 pixelscan 过程中 Timezone 系统时间 还是会暴露地址 应该是跟着 IP 走才对

尝试使用
https://github.com/Stackz7/DiscordTokenGenerator/tree/main
如果成功,使用
https://github.com/wanghaisheng/Botright

This package includes GeoLite data created by MaxMind, available from MaxMind, and also includes IP2Location open source libraries available from IP2Location.

And also thanks for providing these great services and REST APIs for free.

| Provider                               | Supported type | Licence                        |
| -------------------------------------- | -------------- | ------------------------------ |
| [http://freegeoip.net/] [freegeoip]    | IPv4           | free                           |
| [http://ipinfo.io/] [ipinfo]           | IPv4, IPv6     | free                           |
| [http://www.telize.com/] [Telize]      | IPv4, IPv6     | free                           |
| [http://ip-json.rhcloud.com/] [IPJson] | IPv4, IPv6     | free                           |
| [http://ip.pycox.com/] [Pycox]         | IPv4, IPv6     | free                           |
| [http://geoip.nekudo.com/] [Nekudo]    | IPv4, IPv6     | free                           |
| [http://xhanch.com/] [Xhanch]          | IPv4           | free                           |
| [http://www.geoplugin.com/][geoplugin] | IPv4, IPv6     | free, need an attribution link |
| [http://ip-api.com/] [ipapi]           | IPv4, IPv6     | free for non-commercial use    |
| [http://ipinfodb.com/] [IPInfoDB]      | IPv4, IPv6     | free for registered user       |

macbook 使用 clash 代理

1.  https://api64.ipify.org/

无代理
2409:8a70:106f:9ed0:4827:42c3:ebe1:f01f

有代理
38.26.191.97

2.https://jsonip.com/

无代理

{"ip":"2409:8a70:106f:9ed0:4827:42c3:ebe1:f01f","country":"CN","geo-ip":"https://getjsonip.com/#plus","API Help":"https://getjsonip.com/#docs"}

有代理

无法打开

3.https://ipinfo.io/json

无代理：

{
"ip": "111.18.43.23",
"city": "Zhanjiang",
"region": "Guangdong",
"country": "CN",
"loc": "21.2339,110.3875",
"org": "AS9808 China Mobile Communications Group Co., Ltd.",
"timezone": "Asia/Shanghai",
"readme": "https://ipinfo.io/missingauth"
}

有代理

{
"ip": "38.26.191.97",
"city": "Hayward",
"region": "California",
"country": "US",
"loc": "37.6688,-122.0808",
"org": "AS54600 PEG TECH INC",
"postal": "94541",
"timezone": "America/Los_Angeles",
"readme": "https://ipinfo.io/missingauth"
}

4.https://ipapi.co/json/

无代理

{
"ip": "111.18.43.23",
"network": "111.18.32.0/20",
"version": "IPv4",
"city": "Xi'an",
"region": "Shaanxi",
"region_code": "SN",
"country": "CN",
"country_name": "China",
"country_code": "CN",
"country_code_iso3": "CHN",
"country_capital": "Beijing",
"country_tld": ".cn",
"continent_code": "AS",
"in_eu": false,
"postal": null,
"latitude": 34.2635,
"longitude": 108.9246,
"timezone": "Asia/Shanghai",
"utc_offset": "+0800",
"country_calling_code": "+86",
"currency": "CNY",
"currency_name": "Yuan Renminbi",
"languages": "zh-CN,yue,wuu,dta,ug,za",
"country_area": 9596960.0,
"country_population": 1411778724,
"asn": "AS9808",
"org": "China Mobile Communications Group Co., Ltd."
}

使用代理，chrome 打不开

# proxy detect

https://bot.incolumitas.com/proxy_detect.html

https://browserleaks.com/

## Imperva failed on

https://corretor.portoseguro.com.br/corretoronline/

full log

```
Access denied
Error 16
corretor.portoseguro.com.br
2023-06-07 07:12:26 UTC
What happened?
This request was blocked by our security service
Your IP: 194.99.79.70
Proxy IP: 45.223.44.75 (ID 10570-100)
Incident ID: 570000600028606852-21529670364827394
Powered by Imperva
```

https://github.com/aiden2048/Browser-Env






## 步骤一、检测 IP，美国原生IP
* 选取你的美国线路，打开全局代理，确保路线切换为 `美国`（全局模式）；将电脑DNS 改为 `8.8.8.8`和8.8.4.4

![](pic/020.jpg)

* 浏览器 `无痕模式` 打开 [https://whoer.net](https://whoer.net)，检测路线是否被 Google 识别出来。
  
  > * 百分比越高越好，不足地方会列出，如低于 `70%` 建议更换路线<br>
  > * 一定保证IP地址和DNS全部为美国
  > * 最好将系统时间也改为美国时间
  
![](pic/002.jpg)

* 打开 [https://ipdata.co/](https://ipdata.co/)， 输入whoer.net查出来的代理IP地址，测试路线为 `家庭` 或 `托管`。

> * 显示 `type: "isp"` 表示家庭用户，最佳；
> * 显示 `type: "hosting"` 表示代理托管，也能注册成功，但ISP的成功率更大点。