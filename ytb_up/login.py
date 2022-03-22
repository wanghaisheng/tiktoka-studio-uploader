import json
from typing import Dict, List

""" Login module """


def domain_to_url(domain: str) -> str:
    """ Converts a (partial) domain to valid URL """
    if domain.startswith("."):
        domain = "www" + domain
    return "http://" + domain

def login_using_cookie_file(self, cookie_file: str,page):
    """Restore auth cookies from a file. Does not guarantee that the user is logged in afterwards.
    Visits the domains specified in the cookies to set them, the previous page is not restored."""
    domain_cookies: Dict[str, List[object]] = {}
    # cookie_file=r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'
    with open(cookie_file) as file:
        cookies: List = json.load(file)
        # Sort cookies by domain, because we need to visit to domain to add cookies
        for cookie in cookies:
            try:
                domain_cookies[cookie["domain"]].append(cookie)
            except KeyError:
                domain_cookies[cookie["domain"]] = [cookie]
    # print(str(domain_cookies).replace(",", ",\n"))


    for domain, cookies in domain_cookies.items():
        # while True:
        page.goto(domain_to_url(domain + "/robots.txt"))
        for cookie in cookies:
            cookie.pop("sameSite", None)  # Attribute should be available in Selenium >4
            cookie.pop("storeId", None)  # Firefox container attribute
        print('add cookies')
    self.context.add_cookies(cookies)
def confirm_logged_in(page) -> bool:
    """ Confirm that the user is logged in. The browser needs to be navigated to a YouTube page. """
    try:
        print(page.locator("yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"))
        page.locator("yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)")

        # WebDriverWait(page, 10).until(EC.element_to_be_clickable("avatar-btn")))
        return True
    except TimeoutError:
        return False
def confirm_logged_in(page) -> bool:
    """ Confirm that the user is logged in. The browser needs to be navigated to a YouTube page. """
    try:
        print(page.locator("yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"))
        page.locator("yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)")

        # WebDriverWait(page, 10).until(EC.element_to_be_clickable("avatar-btn")))
        return True
    except TimeoutError:
        return False