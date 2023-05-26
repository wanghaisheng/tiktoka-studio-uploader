"""setup script for installing python dependencies in youtube-auto-upload toolkit"""


import subprocess
import time


def checkPLInstalled():

    print('start to check Tiktoka Studio requirements whether playwright intalled')
    
    try:
        from playwright.sync_api import Page, expect, sync_playwright
        return True
    except ImportError as error:
        print(error,':( not found')
        return False
def checkBrowserInstalled():
    
    try:
        print('start to check Tiktoka Studio requirements whether playwright browser intalled')
        
        from playwright.sync_api import sync_playwright    
        with sync_playwright() as p:
            print('start to check Tiktoka Studio requirements whether chromium intalled')
        
            try:
                browser = p.chromium.launch()
                return True
                    
            except:
                return False
            print('start to check Tiktoka Studio requirements whether webkit/edge intalled')
            
            try:
                browser = p.webkit.launch()
                return True
                                    
            except:
                return False
            print('start to check Tiktoka Studio requirements whether firefox intalled')
            
            try:
                browser = p.firefox.launch()
                return True
                                    
            except:
                return False           
    except:
        return False

def attempt(arg_list, max_attempts=1, name=""):
    retries = 0
    while retries < max_attempts:
        proc = subprocess.Popen(arg_list)

        # Keep running until finish or failure (may hang)
        while proc.poll() is None:
            time.sleep(0.1)

        # Proc finished, check for valid return code
        if proc.returncode == 0:
            print(f"\n[INSTALL_PYDEPS] SUCCESS for process '{name}'\n")
            break
        else:
            # Likely failure, retry
            print(f"\n[INSTALL_PYDEPS] FAILURE for process '{name}', retrying!\n")
            retries += 1
    else:
        # Retries exceeded
        raise Exception(f"[INSTALL_PYDEPS] Retries exceeded for proc '{name}'!")


def runPl():
    steps = {
        "step1": """python -m pip install -U pip setuptools wheel""".split(" "),
        "step2": """pip install pytest-playwright""".split(" "),
    }

    for step_name, step_arglist in steps.items():
        print(
            f"\n[INSTALL_PYDEPS] Attempt '{step_name}' -> Run '{' '.join(step_arglist)}'\n"
        )
        attempt(step_arglist, max_attempts=3, name=step_name)

def runBrowser():
    steps = {
        "step1": """playwright install""".split(" "),
    }

    for step_name, step_arglist in steps.items():
        print(
            f"\n[INSTALL_PYDEPS] Attempt '{step_name}' -> Run '{' '.join(step_arglist)}'\n"
        )
        attempt(step_arglist, max_attempts=3, name=step_name)
def getCookie(browserType:str="firefox",proxyserver:str='',channelname:str='youtube-channel'):
    if proxyserver:
        command="playwright codegen -b "+browserType+ " --proxy-server "+proxyserver+" --lang 'en-GB' --save-storage="+channelname+"-cookie.json https://www.youtube.com/upload?persist_gl=1"
    else:
        command="playwright codegen -b "+browserType+" --lang 'en-GB' --save-storage="+channelname+"-cookie.json https://www.youtube.com/upload?persist_gl=1"       
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )


    

    if result.returncode:
        print(f'failed to save cookie file:{result.stderr}')
    else:

        print('just check your cookie file',channelname+'-cookie.json')


if __name__ == "__main__":
    print('start to check Tiktoka Studio requirements whether  intalled')
    
    plinstall=checkPLInstalled()
    browserinstall=checkBrowserInstalled()
    if plinstall==False:
        print('Tiktoka Studio requirements-playwright not intalled')
        
        runPl()
    else:
        print('Tiktoka Studio requirements-playwright have intalled')
    if browserinstall==False:
        print('Tiktoka Studio requirements-browser not intalled')
        
        runBrowser()
    else:
        print('Tiktoka Studio requirements-browser have intalled')        
    # getCookie()
    getCookie('firefox','socks5://127.0.0.1:1080','fastlane')