import json
from typing import Dict, List

""" Login module """


def domain_to_url(domain: str) -> str:
    """ Converts a (partial) domain to valid URL """
    if domain.startswith("."):
        domain = "www" + domain
    return "http://" + domain

async def format_cookie_file(cookie_file: str):
    """Restore auth cookies from a file. Does not guarantee that the user is logged in afterwards.
    Visits the domains specified in the cookies to set them, the previous page is not restored."""
    domain_cookies: Dict[str, List[object]] = {}
    # cookie_file=r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'
    with open(cookie_file) as file:
        cookies: List = json.load(file)
        # Sort cookies by domain, because we need to visit to domain to add cookies
        for cookie in cookies:
            if cookie['sameSite']=='no_restriction' or cookie['sameSite'].lower()=='no_restriction':
                cookie.update(sameSite='None')            
            try:
                domain_cookies[cookie["domain"]].append(cookie)
            except KeyError:
                domain_cookies[cookie["domain"]] = [cookie]
    # print(str(domain_cookies).replace(",", ",\n"))

            # cookie.pop("sameSite", None)  # Attribute should be available in Selenium >4
            # cookie.pop("storeId", None)  # Firefox container attribute
    print('add cookies',domain_cookies[cookie["domain"]])
    # await self.context.add_cookies(cookies)
    return domain_cookies[cookie["domain"]]
def confirm_logged_in(page) -> bool:
    """ Confirm that the user is logged in. The browser needs to be navigated to a YouTube page. """
    try:
        page.locator("yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)")

        # WebDriverWait(page, 10).until(EC.element_to_be_clickable("avatar-btn")))
        return True
    except TimeoutError:
        return False
def confirm_logged_in_douyin(page) -> bool:
    try:

        page.locator('.avatar--1lU_a')
        return True
    except:
        return False

def confirm_logged_in_tiktok(page) -> bool:
    """ Confirm that the user is logged in. The browser needs to be navigated to a YouTube page. """
    try:
        page.locator("yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)")

        return True
    except TimeoutError:
        return False