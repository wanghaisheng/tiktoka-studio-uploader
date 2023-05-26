"""setup script for installing python dependencies in youtube-auto-upload toolkit"""


import subprocess
import time


def checkInstalled():


    try:
        from playwright.sync_api import Page, expect
    except ImportError as error:
        print(error,':( not found')
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


def run():
    steps = {
        "step1": """python -m pip install -U pip setuptools wheel""".split(" "),
        "step2": """pip install pytest-playwright""".split(" "),
        "step3": """playwright install""".split(" "),
    }

    for step_name, step_arglist in steps.items():
        print(
            f"\n[INSTALL_PYDEPS] Attempt '{step_name}' -> Run '{' '.join(step_arglist)}'\n"
        )
        attempt(step_arglist, max_attempts=3, name=step_name)


def getCookie(browserType:str="firefox",proxyserver:str='',channelname:str='youtube-channel'):
    if proxyserver:
        command='playwright codegen -b '+browserType+ ' --proxy-server '+proxyserver+' --lang "en-GB" --save-storage='+channelname+'-cookie.json https://www.youtube.com/upload?persist_gl=1'
    else:
        command='playwright codegen -b '+browserType+' --lang "en-GB" --save-storage='+channelname+'-cookie.json https://www.youtube.com/upload?persist_gl=1'        
    # print(command)
    is_corrupted = subprocess.call(
        # 'ffprobe -i "' + fullpath + '"',
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # print(is_corrupted)

    if is_corrupted:
        print('bingo')
    # Fix bad files
    else:
        print('just check your cookie file',channelname+'-cookie.json')


if __name__ == "__main__":
    install=checkInstalled()
    if install==False:
        run()
    # getCookie()
    getCookie('firefox','socks5://127.0.0.1:1080','fastlane')