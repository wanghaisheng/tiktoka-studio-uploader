"""Gets the browser's given the user's input"""
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Webdriver managers
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService

from selenium import webdriver
from seleniumbase import SB

from upgenius.tiktok.selenium import config
from upgenius.tiktok.selenium.proxy_auth_extension.proxy_auth_extension import generate_proxy_auth_extension


def get_browser(name: str = 'chrome',headless=False,proxy=None, options=None, *args, **kwargs) -> webdriver:
    """
    Gets a browser based on the name with the ability to pass in additional arguments
    """
    with SB(uc=True,xvfb=True,browser=name, test=True,proxy=proxy,headless=headless) as sb:
        return sb.get_new_driver(
    locale_code=None,
    protocol=None,
    servername=None,
    port=None,
    # proxy=None,
    proxy_bypass_list=None,
    proxy_pac_url=None,
    multi_proxy=None,
    agent=None,
    switch_to=True,
    cap_file=None,
    cap_string=None,
    recorder_ext=None,
    disable_js=None,
    disable_csp=None,
    enable_ws=None,
    enable_sync=None,
    use_auto_ext=None,
    undetectable=None,
    uc_cdp_events=None,
    uc_subprocess=None,
    log_cdp_events=None,
    no_sandbox=None,
    disable_gpu=None,
    headless2=None,
    incognito=None,
    guest_mode=None,
    dark_mode=None,
    devtools=None,
    remote_debug=None,
    enable_3d_apis=None,
    swiftshader=None,
    ad_block_on=None,
    block_images=None,
    do_not_track=None,
    chromium_arg=None,
    firefox_arg=None,
    firefox_pref=None,
    user_data_dir=None,
    extension_zip=None,
    extension_dir=None,
    binary_location=None,
    driver_version=None,
    page_load_strategy=None,
    use_wire=None,
    external_pdf=None,
    is_mobile=None,
    d_width=None,
    d_height=None,
    d_p_r=None) 

            


def get_driver(name: str = 'chrome', *args, **kwargs) -> webdriver:
    """
    Gets the web driver function for the browser
    """
    if _clean_name(name) in drivers:
        return drivers[name]

    raise UnsupportedBrowserException()


def get_service(name: str = 'chrome'):
    """
    Gets a service to install the browser driver per webdriver-manager docs

    https://pypi.org/project/webdriver-manager/
    """
    if _clean_name(name) in services:
        return services[name]()

    return None # Safari doesn't need a service


def get_default_options(name: str, *args, **kwargs):
    """
    Gets the default options for each browser to help remain undetected
    """
    name = _clean_name(name)

    if name in defaults:
        return defaults[name](*args, **kwargs)

    raise UnsupportedBrowserException()


def chrome_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> ChromeOptions:
    """
    Creates Chrome with Options
    """

    options = ChromeOptions()

    ## regular
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--profile-directory=Default')

    ## experimental
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    ## add english language to avoid languages translation error
    options.add_argument("--lang=en")

    # headless
    if headless:
        options.add_argument('--headless=new')
    if proxy:
        if 'user' in proxy.keys() and 'pass' in proxy.keys():
            # This can fail if you are executing the function more than once in the same time
            extension_file = 'temp_proxy_auth_extension.zip'
            print(f'proxy with user pass gen proxy extension :{proxy}')
            generate_proxy_auth_extension(proxy['scheme'],proxy['host'], proxy['port'], proxy['user'], proxy['pass'], extension_file)
            options.add_extension(extension_file)
        else:
            print('proxy without user pass',f'--proxy-server={proxy["scheme"]}://{proxy["host"]}:{proxy["port"]}')
            options.add_argument(f'--proxy-server={proxy["scheme"]}://{proxy["host"]}:{proxy["port"]}')
            # options.add_argument('--proxy-server=socks5://' + '127.0.0.1:1080')

    return options


def firefox_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> FirefoxOptions:
    """
    Creates Firefox with default options
    """

    options = FirefoxOptions()

    # default options

    if headless:
        options.add_argument('--headless')
    if proxy:
        raise NotImplementedError('Proxy support is not implemented for this browser')
    return options


def safari_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> SafariOptions:
    """
    Creates Safari with default options
    """
    options = SafariOptions()

    # default options

    if headless:
        options.add_argument('--headless')
    if proxy:
        raise NotImplementedError('Proxy support is not implemented for this browser')
    return options


def edge_defaults(*args, headless: bool = False, proxy: dict = None, **kwargs) -> EdgeOptions:
    """
    Creates Edge with default options
    """
    options = EdgeOptions()

    # default options

    if headless:
        options.add_argument('--headless')
    if proxy:
        raise NotImplementedError('Proxy support is not implemented for this browser')
    return options

# Misc
class UnsupportedBrowserException(Exception):
    """
    Browser is not supported by the library

    Supported browsers are:
        - Chrome
        - Firefox
        - Safari
        - Edge
    """

    def __init__(self, message=None):
        super().__init__(message or self.__doc__)


def _clean_name(name: str) -> str:
    """
    Cleans the name of the browser to make it easier to use
    """
    return name.strip().lower()


drivers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'safari': webdriver.Safari,
    'edge': webdriver.ChromiumEdge,
}

defaults = {
    'chrome': chrome_defaults,
    'firefox': firefox_defaults,
    'safari': safari_defaults,
    'edge': edge_defaults,
}


services = {
    'chrome': lambda : ChromeService(ChromeDriverManager().install()),
    'firefox': lambda : FirefoxService(GeckoDriverManager().install()),
    'edge': lambda : EdgeService(EdgeChromiumDriverManager().install()),
}