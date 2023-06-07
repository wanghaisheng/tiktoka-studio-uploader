import httpx
from async_class import AsyncObject, link
import requests

class SplitError(Exception):
    pass


class ProxyCheckError(Exception):
    pass


class ProxyManager(AsyncObject):
    async def __ainit__(self, botright, proxy) -> None:
        link(self, botright)

        self.proxy = proxy.strip() if proxy else None
        self.http_proxy = None
        self.ip = None
        self.port = None
        self.username = None
        self.password = None
        self.browser_proxy = None
        self.plain_proxy = None
        self.timeout = httpx.Timeout(20.0, read=None)
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
                # context_proxy = ProxySettings(server=self.proxy)
                pass
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
                    # context_proxy = ProxySettings(server=self.proxy)
                    pass
                else:
                    raise GeneratorExit(f"Proxy Format ({self.proxy}) isnt supported")
        elif len(splitted) == 4:
            self.split_helper(splitted)
        else:
            if "socks5" in self.proxy:
                # context_proxy = ProxySettings(server=self.proxy)
                pass
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


    def searchIPWithFile(self,ip):
        # 1. 创建查询对象
        dbPath = "ip2region.xdb"
        dbPath = os.path.join(
        os.path.dirname(__file__), "../txt/" + dbPath
    )       
        searcher = XdbSearcher(dbfile=dbPath)
        
        # 2. 执行查询
        ip = "1.2.3.4"
        region_str = searcher.searchByIPStr(ip)
        print(region_str)
        
        # 3. 关闭searcher
        searcher.close()
    def valid_ipv4(self,IP):
          segement = IP.split('.')
          if len(segement) == 4:
              for s_str in segement:
                  if 0 < len(s_str) < 4:
                      for s in s_str:
                          if not s.isdigit():
                              return False
                      if len(s_str) > 1 and s_str[0] == '0' or int(s_str) > 255:
                          return False
                  else:
                      return False
          else:
              return False

          return True


    def valid_ipv6(self,IP):
          set_chars = '0123456789abcdefABCDEF'
          segement = IP.split(':')
          if len(segement) == 8:
              for seg_str in segement:
                  if 0 < len(seg_str) < 5:
                      for s in seg_str:
                          if s not in set_chars:
                              return False
                      
                      # make sure no multi '0'
                    #   not sure why test case didn't check '0000'
                      if len(seg_str) > 1 and seg_str[0] == '0' and seg_str[1] == '0':
                          print(2)
                          return False

                  else:
                      return False

          else:
              return False

          return True



    def check_proxy(self):
        ip = None
        try:
            print("self.httpx_proxy,", type(self.httpx_proxy), self.httpx_proxy)
            # ip_request = requests.get(
            #     "https://jsonip.com",
            #     proxies=self.httpx_proxy if self.httpx_proxy else None,
            # )
# https://ipapi.co/json/

            ip_request = requests.get(
                "https://ipapi.co/json/",
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )
            print('====1====',ip_request.content)
            print('====2====',ip_request.text)
            
            print(ip_request.status_code)
            if ip_request.status_code == 200:
                ip = ip_request.json().get("ip")
                if self.valid_ipv4(ip)==False:
                    res=self.searchIPWithFile(ip)
                    print('{}')
                else:
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