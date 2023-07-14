"""setup script for installing python dependencies in youtube-auto-upload toolkit"""


import subprocess
import time

from typing import Tuple, Optional, Union, Literal

def checkPLInstalled():
    print("start to check Tiktoka Studio requirements whether playwright intalled")

    try:
        from playwright.sync_api import Page, expect, sync_playwright

        return True
    except ImportError as error:
        print(error, ":( not found")
        return False


def checkBrowserInstalled(browserType:Literal["chromium", "firefox", "webkit"] = "firefox"):
    try:
        print(
            "start to check Tiktoka Studio requirements whether playwright browser intalled"
        )
        from playwright.sync_api import sync_playwright

        print("import pl library")

        with sync_playwright() as p:
            print("initial pl library")

            try:
                print(f"start to check Tiktoka Studio requirements whether {browserType} intalled")
                browser = p.browserType.launch()
                print(f"{browserType}  intalled")

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


def runBrowser(browserType:Literal["chromium", "firefox", "webkit"] = None):
    if browserType==None:
        steps = {
            "step1": """playwright install""".split(" "),
        }
        print(f'install all type browsers')

    else:
        steps = {
            "step1": ("""playwright install """+ browserType).split(" "),
        }        
        print(f'install browsertype {browserType}')

    for step_name, step_arglist in steps.items():
        print(
            f"\n[INSTALL_PYDEPS] Attempt '{step_name}' -> Run '{' '.join(step_arglist)}'\n"
        )
        attempt(step_arglist, max_attempts=3, name=step_name)


def checkRequirments(browserType:Literal["chromium", "firefox", "webkit"] = None):
    print("start to check Tiktoka Studio requirements whether  intalled")

    plinstall = checkPLInstalled()
    if plinstall == False:
        print("Tiktoka Studio requirements-playwright not intalled")

        runPl()
    else:
        print("Tiktoka Studio requirements-playwright have intalled")
    if browserType==None:
        runBrowser()
    if browserType=="chromium":

        browserinstall = checkBrowserInstalled(browserType="chromium")

        if browserinstall == False:
            print(f"Tiktoka Studio requirements-browser {browserType} not intalled")

            runBrowser("chromium")
            print(f"Tiktoka Studio requirements-auto browser {browserType} intalled")

        else:
            print(f"Tiktoka Studio requirements-browser {browserType} have intalled")
    if browserType=="firefox":

        browserinstall = checkBrowserInstalled(browserType="firefox")

        if browserinstall == False:
            print(f"Tiktoka Studio requirements-browser {browserType} not intalled")

            runBrowser("firefox")
            print(f"Tiktoka Studio requirements-auto browser {browserType} intalled")

        else:
            print(f"Tiktoka Studio requirements-browser {browserType} have intalled")
    if browserType=="webkit":

        browserinstall = checkBrowserInstalled(browserType="webkit")

        if browserinstall == False:
            print(f"Tiktoka Studio requirements-browser {browserType} not intalled")

            runBrowser("webkit")
            print(f"Tiktoka Studio requirements-auto browser {browserType} intalled")

        else:
            print(f"Tiktoka Studio requirements-browser {browserType} have intalled")
